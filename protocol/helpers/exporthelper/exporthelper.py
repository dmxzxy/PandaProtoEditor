#!/usr/bin/env python
# -*- encoding:utf8 -*-

import customadapter
from protocol.helpers.panpbtool import panpbtool

def export(branch, out_dir):
    project = customadapter.translate(branch)
    panpbtool.write(out_dir, project)