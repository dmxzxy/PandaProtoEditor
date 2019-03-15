#!/usr/bin/env python
# -*- encoding:utf8 -*-

from protocol.models import ProtocolLabel
from protocol.models import FieldLabel
from protocol.models import FieldType
from protocol.models import Message
from protocol.models import Protocol
from protocol.models import Module


def reset(branch):
    modules = Module.objects.filter(project = branch)
    modules.delete()