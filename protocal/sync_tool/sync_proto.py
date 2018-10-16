import json
import os
import shutil
import time
import traceback, sys

from string import strip

from protocal.models import *
from protocal.utils import cmd_call
from protocal.utils import get_file_list

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

PROTOC_BIN_NAME = 'win32/protoc.exe'


class cls_context:
    project = None
    branche = None
    setting = None

    def __str__(self):
        return self.project.title


def do_parse_proto_files(context):
    proto_sync_path = context.proto_sync_path
    file_list = get_file_list(proto_sync_path, ['proto'])

    proto_bin = context.bin_path + PROTOC_BIN_NAME
    proto_parse_out = ""
    plugin_execute = ""
    cmdHead = "%s -I=%s --parse_out=%s --plugin=protoc-gen-parse=%s " % (
        proto_bin, proto_sync_path, proto_parse_out, plugin_execute)

    cmd = cmdHead
    for f in file_list:
        cmd += f
        cmd += ' '
    cmd_call(cmd)


def do_sync(project, branche):
    context = cls_context()
    context.project = project
    context.branche = branche
    bin_path = os.path.dirname(__file__)
    bin_path = os.path.abspath(bin_path+'/../')
    context.bin_path = bin_path + "/bin/"
    pass
