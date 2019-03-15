#!/usr/bin/env python
# -*- encoding:utf8 -*-

import customadapter
import resetdb

from customrule import customrule
from protocol.helpers.panpbtool import panpbtool

def sync(project, branch, src_dir):
    midproject = panpbtool.read(src_dir, customrule)
    resetdb.reset(branch)
    customadapter.translate(branch, midproject)