#!/usr/bin/env python
# -*- encoding:utf8 -*-

from django.shortcuts import get_object_or_404

from protocol.models import ProtocolLabel
from protocol.models import FieldLabel
from protocol.models import FieldType
from protocol.models import Message
from protocol.models import Protocol

from protocol.helpers.panpbtool.data import middata
from protocol.helpers.panpbtool.conf import prototype
from protocol.helpers.panpbtool.conf import protolabel

class translater():
    branch = None
    data = None
    def __init__(self, branch, data):
        self.branch = branch
        self.data = data

    def dotrans(self):
        for module_data in self.data.modules:
            self._dotrans_module(module_data)

        self._dotrans_allfield()

    def _dotrans_allfield(self):
        for module_data in self.data.modules:
            for message_data in module_data.messages:
                self._dotrans_allmessagefields(message_data)
            for protocol_data in module_data.protocols:
                self._dotrans_allmessagefields(protocol_data)
    
    def _dotrans_allmessagefields(self, message_data):
        message = get_object_or_404(Message, fullname=message_data.fullname)
        for message_data in message_data.nested_messages:
            self._dotrans_allmessagefields(message_data)
        for field_data in message_data.fields:
            self._dotrans_messagefield(message, field_data)


    def _dotrans_module(self, module_data):
        branch = self.branch
        
        module_desc = self.data.get_comment(module_data.location)
        if len(module_desc) == 0:
            module_desc = module_data.name

        module = branch.module_set.create(
            project = branch,
            name = module_data.name,
            fullname = module_data.fullname,
            desc = module_desc,
        )

        for message_data in module_data.messages:
            self._dotrans_message(module, None, False, message_data)
            
        for enum_data in module_data.enums:
            self._dotrans_enum(module, None, enum_data)
            
        for protocol_data in module_data.protocols:
            self._dotrans_message(module, None, True, protocol_data)

    def _dotrans_message(self, module, nested_msg, isproto, message_data):
        message_desc = self.data.get_comment(message_data.location)
        if len(message_desc) == 0:
            message_desc = message_data.name
        
        message = module.message_set.create(
            module = module,
            name = message_data.name,
            fullname = message_data.fullname,
            desc = message_desc,
            nested = nested_msg
        )

        if isproto:
            protocol = Protocol(
                message = message,
                protocol_id = message_data.id,
                protocol_ref = None,
                protocol_label = get_object_or_404(ProtocolLabel, name=message_data.category),
            )
            protocol.save()
        else:
            module.fieldtype_set.create(
                type = prototype.ProtocolType.TYPE_MESSAGE,
                typename = message_data.fullname,
                desc = message_desc,
                priority = 2
            )

        for message_data in message_data.nested_messages:
            self._dotrans_message(module, message, False, message_data)
            
        for enum_data in message_data.nested_enums:
            self._dotrans_enum(module, message, enum_data)

        # for field_data in message_data.fields:
        #     self._dotrans_messagefield(module, message, field_data)

    def _dotrans_messagefield(self, message, field_data):
        field_desc = self.data.get_comment(field_data.location)
        if len(field_desc) == 0:
            field_desc = field_data.name

        field_type = None
        proto_type = field_data.proto_type
        if proto_type.is_basic:
            field_type = get_object_or_404(FieldType, type=proto_type.id)
        else:
            field_type = get_object_or_404(FieldType, typename=proto_type.name)
            
        message.field_set.create(
            name = field_data.name,
            fullname = field_data.fullname,
            desc = field_desc,
            label = get_object_or_404(FieldLabel, name=protolabel.get_name(field_data.label)),
            type = field_type,
            number= field_data.number,
        )
        
    def _dotrans_enum(self, module, nested_msg, enum_data):
        #TODO
        pass
    
    def _dotrans_enumfield(self, module, field_data):
        #TODO
        pass

def translate(branch, data):
    trans = translater(branch, data)
    trans.dotrans()