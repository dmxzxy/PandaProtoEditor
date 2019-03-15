#!/usr/bin/env python
# -*- encoding:utf8 -*-

import customadapter
from protocol.helpers.panpbtool import panpbtool

def export(out_dir):
    project = customadapter.translate()
    panpbtool.write(out_dir, project)