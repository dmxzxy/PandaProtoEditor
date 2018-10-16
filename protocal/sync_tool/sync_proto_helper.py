# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from protocal.utils import get_file_list
from protocal.utils import cmd_call

import os
import json
import sync_proto
import protocal.project_helper

import sys
reload(sys)
sys.setdefaultencoding('utf8')

PROTOC_BIN_NAME = 'win32/protoc.exe'


class context_setting:
    pass


class cls_context:
    project = None
    branche = None
    setting = None
    proto_sync_path = None

    def __str__(self):
        return self.project.title


def do_update_proto(context):
    setting = context.setting
    proto_sync_path = setting.proto_sync_path
    branche = context.branche

    cmd = "svn co %s %s --username zhangxiaoyu --password XgQh8qmGPJI4" % (
        branche.proto_url, proto_sync_path)
    cmd_call(cmd.encode("gbk"))


def do_parse_proto_files(context):
    setting = context.setting

    proto_sync_path = setting.proto_sync_path
    file_list = get_file_list(proto_sync_path, 'proto')

    proto_bin = setting.bin_path + PROTOC_BIN_NAME
    proto_parse_out = setting.proto_parse_path
    plugin_execute = setting.proto_plugin

    if not os.path.exists(proto_parse_out):
        os.makedirs(proto_parse_out)

    cmdHead = "%s -I=%s --parse_out=%s --plugin=protoc-gen-parse=%s " % (
        proto_bin, proto_sync_path, proto_parse_out, plugin_execute)

    cmd = cmdHead
    for f in file_list:
        cmd += f
        cmd += ' '
    cmd_call(cmd)


def sync(project, branche):
    # build context
    context = cls_context()
    context.project = project
    context.branche = branche

    branch_path = protocal.project_helper.get_branche_path(branche.id)

    if not os.path.exists(branch_path):
        os.makedirs(branch_path)

    setting = context_setting()
    setting.bin_path = os.path.dirname(__file__) + '/../bin/'
    setting.proto_sync_path = branch_path + '/proto/'
    setting.proto_parse_path = branch_path + '/proto_parse/'
    setting.proto_plugin = os.path.dirname(__file__) + "/plugin/runparse.bat"
    context.setting = setting

    do_update_proto(context)

    do_parse_proto_files(context)

    with open(setting.proto_parse_path + '/' + 'parse.json', 'r') as load_f:
        proto_parse_dict = json.load(load_f)
        context.proto_parse_dict = proto_parse_dict

    sync_proto.do_sync(context)