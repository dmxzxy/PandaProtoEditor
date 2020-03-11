#!/usr/bin/env python
# -*- encoding:utf8 -*-

import time
import customadapter
import resetdb
from summary_tools import *

from customrule import customrule
from protocol.helpers.panpbtool import panpbtool

def sync(project, branch, src_dir):
    print("[syncHelper] start sync")

    print("[syncHelper] read protocol")
    midproject = panpbtool.read(src_dir, customrule)
    print("[syncHelper] reset database")
    resetdb.reset(branch)
    print("[syncHelper] start translate")
    customadapter.translate(branch, midproject)
    print("[syncHelper] end sync")