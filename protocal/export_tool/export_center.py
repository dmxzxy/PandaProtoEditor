import json
import os
import shutil
from time import sleep
import traceback, sys

from protocal.models import *

class cls_context:
    project = None
    setting = None
    def __str__(self):
        return self.project.title

def do_export(project, branche, version, export_setting):
    context = cls_context()