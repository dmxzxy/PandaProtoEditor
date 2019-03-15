#!/usr/bin/env python
# -*- encoding:utf8 -*-

import protocol.utils

default_acc = "zhangxiaoyu"
default_pwd = "XgQh8qmGPJI4"

def doupdate(url, path):
    cmd = "svn co %s %s --username %s --password %s" % (url, path, default_acc, default_pwd)
    protocol.utils.cmd_call(cmd.encode("gbk"))