#!/usr/bin/env python
# -*- encoding:utf8 -*-

from django.shortcuts import get_object_or_404

from protocol.models import ProtocolLabel
from protocol.models import FieldLabel
from protocol.models import FieldType
from protocol.models import Message
from protocol.models import Protocol
from protocol.models import Field
from protocol.models import Enum
from protocol.models import EnumValue

from protocol.helpers.panpbtool.data import middata
from protocol.helpers.panpbtool.conf import prototype
from protocol.helpers.panpbtool.conf import protolabel

class translater():
    branch = None
    data = None

    field_collect = None
    enumvalue_collect = None
    protocol_collect = None

    def __init__(self, branch, data):
        self.branch = branch
        self.data = data
        
        self.field_collect = []
        self.protocol_collect = []
        self.enumvalue_collect = []

    def dotrans(self):
        print("[translater] start dotrans")
        
        for module_data in self.data.modules:
            self._dotrans_module(module_data)

        self._dotrans_allfield()

        self._dotrans_allenumvalue()

        self._dotrans_allprotocol()

        Field.objects.bulk_create(self.field_collect)
        Protocol.objects.bulk_create(self.protocol_collect)
        EnumValue.objects.bulk_create(self.enumvalue_collect)
        print("[translater] end dotrans")

    def _dotrans_allfield(self):
        for module_data in self.data.modules:
            for message_data in module_data.messages:
                self._dotrans_allmessagefields(message_data)
            for protocol_data in module_data.protocols:
                self._dotrans_allmessagefields(protocol_data)
    
    def _dotrans_allmessagefields(self, message_data):
        message = get_object_or_404(Message, module__project=self.branch, fullname=message_data.fullname)
        for child_message_data in message_data.nested_messages:
            self._dotrans_allmessagefields(child_message_data)
        for field_data in message_data.fields:
            self._dotrans_messagefield(message, field_data)

    def _dotrans_allprotocol(self):
        for module_data in self.data.modules:
            for protocol_data in module_data.protocols:
                message = get_object_or_404(Message, module__project=self.branch, fullname=protocol_data.fullname)
                protocol = Protocol(
                    message = message,
                    protocol_id = protocol_data.id,
                    protocol_ref = None,
                    protocol_label = get_object_or_404(ProtocolLabel, name=protocol_data.category),
                )
                self.protocol_collect.append(protocol)

    def _dotrans_allenumvalue(self):
        for module_data in self.data.modules:
            for enum_data in module_data.enums:
                enum = get_object_or_404(Enum, module__project=self.branch, fullname=enum_data.fullname)
                for value_data in enum_data.values:
                    enumvalue_desc = self.data.get_comment(value_data.location)
                    if len(enumvalue_desc) == 0:
                        enumvalue_desc = value_data.name

                    newValue = EnumValue(
                        enum = enum,
                        name = value_data.name,
                        fullname = value_data.fullname,
                        desc = enumvalue_desc,
                        number = value_data.number
                    )
                    self.enumvalue_collect.append(newValue)
        

    def _dotrans_module(self, module_data):
        print("[translater] *start module name = " + module_data.name)
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

        fieldtype_collect = []
        msg_collect = []
        enum_collect = []
        for message_data in module_data.messages:
            self._dotrans_message(module, None, False, message_data, fieldtype_collect, msg_collect, enum_collect)
        
        for enum_data in module_data.enums:
            self._dotrans_enum(module, None, enum_data, fieldtype_collect, enum_collect)
            
        for protocol_data in module_data.protocols:
            self._dotrans_message(module, None, True, protocol_data, fieldtype_collect, msg_collect, enum_collect)

        FieldType.objects.bulk_create(fieldtype_collect)
        Message.objects.bulk_create(msg_collect)
        Enum.objects.bulk_create(enum_collect)
        print("[translater] #end module name = " + module_data.name)

    def _dotrans_message(self, module, nested_msg, isproto, message_data, fieldtype_collect, msg_collect, enum_collect):
        message_desc = self.data.get_comment(message_data.location)
        if len(message_desc) == 0:
            message_desc = message_data.name
        
        if nested_msg == None and len(message_data.nested_messages) == 0:
            message = Message(
                module = module,
                name = message_data.name,
                fullname = message_data.fullname,
                desc = message_desc,
                nested = None
            )
            msg_collect.append(message)
        else:
            message = module.message_set.create(
                module = module,
                name = message_data.name,
                fullname = message_data.fullname,
                desc = message_desc,
                nested = nested_msg
            )

        if not isproto:
            fieldtype = FieldType(
                module = module,
                type = prototype.ProtocolType.TYPE_MESSAGE,
                typename = message_data.fullname,
                desc = message_desc,
                priority = 2
            )
            fieldtype_collect.append(fieldtype)

        for child_message_data in message_data.nested_messages:
            self._dotrans_message(module, message, False, child_message_data, fieldtype_collect, msg_collect, enum_collect)
            
        for child_enum_data in message_data.nested_enums:
            self._dotrans_enum(module, message, child_enum_data, fieldtype_collect, enum_collect)

    fieldlabelcache = None
    def _get_fieldlabel(self, label):
        if self.fieldlabelcache == None:
            self.fieldlabelcache = {}
        if str(label) not in self.fieldlabelcache:
            self.fieldlabelcache[str(label)] = get_object_or_404(FieldLabel, name=protolabel.get_name(label))
        return self.fieldlabelcache[str(label)]

    fieldtypecache = None
    def _get_fieldtype(self, proto_type):
        if self.fieldtypecache == None:
            self.fieldtypecache = {}

        if proto_type.name in self.fieldtypecache:
            return self.fieldtypecache[proto_type.name]

        if proto_type.is_basic:
            fieldtype = get_object_or_404(FieldType, type=proto_type.id)
            self.fieldtypecache[proto_type.name] = fieldtype
            return fieldtype
        else: 
            fieldtype = get_object_or_404(FieldType, module__project=self.branch, typename=proto_type.name)
            self.fieldtypecache[proto_type.name] = fieldtype
            return fieldtype

    def _dotrans_messagefield(self, message, field_data):
        print("[translater] ***start field name = " + message.name + "." + field_data.name)
        field_desc = self.data.get_comment(field_data.location)
        if len(field_desc) == 0:
            field_desc = field_data.name
   
        field_type = self._get_fieldtype(field_data.proto_type)    
        field_label = self._get_fieldlabel(field_data.label)

        newfield = Field(
            message = message,
            name = field_data.name,
            fullname = field_data.fullname,
            desc = field_desc,
            label = field_label,
            type = field_type,
            number = field_data.number,
        )
        self.field_collect.append(newfield)
        print("[translater] ###end field name = " + message.name + "." + field_data.name)
        
    def _dotrans_enum(self, module, nested_msg, enum_data, fieldtype_collect, enum_collect):
        enum_desc = self.data.get_comment(enum_data.location)
        if len(enum_desc) == 0:
            enum_desc = enum_data.name

        fieldtype = FieldType(
            module = module,
            type = prototype.ProtocolType.TYPE_ENUM,
            typename = enum_data.fullname,
            desc = enum_desc,
            priority = 2
        )
        fieldtype_collect.append(fieldtype)

        newEnum = Enum(
            module = module,
            name = enum_data.name,
            fullname = enum_data.fullname,
            desc = enum_desc,
            nested = nested_msg
        )
        enum_collect.append(newEnum)
    

def translate(branch, data):
    trans = translater(branch, data)
    trans.dotrans()