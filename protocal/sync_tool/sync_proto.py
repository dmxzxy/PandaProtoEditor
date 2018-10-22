from string import strip

from protocal.models import ProtocalLabel
from protocal.models import FieldLabel
from protocal.models import FieldType
from protocal.models import Message
from protocal.models import Protocal

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

import re


class Field_Type:
    TYPE_DOUBLE = 1
    TYPE_FLOAT = 2
    TYPE_INT64 = 3
    TYPE_UINT64 = 4
    TYPE_INT32 = 5
    TYPE_FIXED64 = 6
    TYPE_FIXED32 = 7
    TYPE_BOOL = 8
    TYPE_STRING = 9
    TYPE_GROUP = 10
    TYPE_MESSAGE = 11
    TYPE_BYTES = 12
    TYPE_UINT32 = 13
    TYPE_ENUM = 14
    TYPE_SFIXED32 = 15
    TYPE_SFIXED64 = 16
    TYPE_SINT32 = 17
    TYPE_SINT64 = 18


class Label_Type:
    LABEL_OPTIONAL = 1
    LABEL_REQUIRED = 2
    LABEL_REPEATED = 3


LabelName = {
    Label_Type.LABEL_OPTIONAL: 'optional',
    Label_Type.LABEL_REQUIRED: 'required',
    Label_Type.LABEL_REPEATED: 'repeated',
}


class MessageParseDefault():
    def __init__(self, context, message_dict):
        self.context = context
        self.message_dict = message_dict

    def is_protocal(self):
        message_name = self.message_dict['name']
        if message_name.startswith('C2S') or message_name.startswith('S2C'):
            return True

        message_desc = self.message_dict['desc']
        ids = re.findall(r'_id\("(.*?)"\)', message_desc, re.MULTILINE)
        return len(ids) > 0

    def get_protocal_id(self):
        proto_ids_parse = self.context.proto_ids_parse
        message_name = self.message_dict['name'].lower()
        if message_name in proto_ids_parse:
            id = proto_ids_parse[message_name]['id']
            if id is not None:
                return id
        else:
            print(message_name + " can not find id")
            return 0

        message_desc = self.message_dict['desc']
        ids = re.findall(r'_id\("(.*?)"\)', message_desc, re.MULTILINE)
        if len(ids) > 0:
            return ids[0]
        return 0

    def get_protocal_label(self):
        message_name = self.message_dict['name']

        if message_name.startswith('C2S'):
            return ProtocalLabel.objects.get(name="Request")

        if message_name.startswith('S2C'):
            return ProtocalLabel.objects.get(name="Response")

        return ProtocalLabel.objects.get(name="Notification")


# sync


def _do_sync_enum_value(context, module, enum_dict):
    pass


def _do_sync_enum(context, module, nested_msg, enum_dict):
    pass


def _do_sync_message_field(context, message, field_dict):
    field_name = field_dict['name']
    field_fullname = field_dict['fullname']
    field_desc = field_dict['desc']
    if len(field_desc) == 0:
        field_desc = field_name
    field_label = field_dict['label']
    field_type = field_dict['type']
    field_number = field_dict['number']

    if field_type == Field_Type.TYPE_ENUM:
        field_type = get_object_or_404(
            FieldType, typename=field_dict['type_name'][1:])
    elif field_type == Field_Type.TYPE_MESSAGE:
        field_type = get_object_or_404(
            FieldType, typename=field_dict['type_name'][1:])
    else:
        field_type = get_object_or_404(FieldType, type=field_type)

    message.field_set.create(
        name=field_name,
        fullname=field_fullname,
        desc=field_desc,
        label=get_object_or_404(FieldLabel, name=LabelName[field_label]),
        type=field_type,
        number=field_number,
    )


def _do_sync_message(context, module, nested_msg, message_dict):
    message_name = message_dict['name']
    message_desc = message_dict['desc']
    if len(message_desc) == 0:
        message_desc = message_name
    message_fullname = message_dict['fullname']
    message = module.message_set.create(
        module=module,
        name=message_name,
        fullname=strip(message_fullname),
        desc=message_desc,
        nested=nested_msg
    )

    parse = MessageParseDefault(context, message_dict)
    if parse.is_protocal():
        protocal = Protocal(
            message=message,
            protocal_id=parse.get_protocal_id(),
            protocal_ref=None,
            protocal_label=parse.get_protocal_label(),
        )
        protocal.save()
    else:
        module.fieldtype_set.create(
            type=Field_Type.TYPE_MESSAGE,
            typename=message_fullname,
            desc=message_desc,
            priority=2)
        
    for enum_dict in message_dict['enumlist']:
        _do_sync_enum(context, module, message, enum_dict)

    for nested_msg_dict in message_dict['nestedtypelist']:
        _do_sync_message(context, module, message, nested_msg_dict)

    # for field_dict in message_dict['fieldlist']:
    #     _do_sync_message_field(context, message, field_dict)


def _do_sync_only_message_field(context, message_dict):
    message = get_object_or_404(Message, fullname=message_dict['fullname'])
    for nested_msg_dict in message_dict['nestedtypelist']:
        _do_sync_only_message_field(context, nested_msg_dict)

    for field_dict in message_dict['fieldlist']:
        _do_sync_message_field(context, message, field_dict)


def _do_sync_module(context, module_dict):
    cur_branche = context.branche
    proj_namespace = context.project.namespace
    module_fullname = module_dict['package']
    module_name = module_fullname.replace(proj_namespace + '.', '')
    module_desc = module_name

    if proj_namespace == module_fullname:
        module_name = 'global'
        module_desc = 'global'

    module = cur_branche.module_set.create(
        project=cur_branche,
        name=module_name,
        fullname=strip(module_fullname),
        desc=module_desc,
    )

    for enum_dict in module_dict['enumlist']:
        _do_sync_enum(context, module, None, enum_dict)

    for message_dict in module_dict['messagelist']:
        _do_sync_message(context, module, None, message_dict)


def _do_sync_branche(context):
    proto_parse_dict = context.proto_parse_dict
    for module_dict in proto_parse_dict['modulelist']:
        _do_sync_module(context, module_dict)

    for module_dict in proto_parse_dict['modulelist']:
        for message_dict in module_dict['messagelist']:
            _do_sync_only_message_field(context, message_dict)


def do_sync(context):
    _do_sync_branche(context)
