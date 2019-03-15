# -*- coding: utf-8 -*-

from django.db.models.signals import post_migrate

from protocol.models import FieldLabel
from protocol.models import ProtocolLabel
from protocol.models import FieldType
 
def init_db(sender, **kwargs):
    if sender.name == 'protocol':
        if not FieldLabel.objects.exists():
            FieldLabelList = []
            FieldLabelList.append(FieldLabel(name = "optional", desc = "optional"))
            FieldLabelList.append(FieldLabel(name = "required", desc = "required"))
            FieldLabelList.append(FieldLabel(name = "repeated", desc = "repeated"))
            FieldLabel.objects.bulk_create(FieldLabelList)

        if not ProtocolLabel.objects.exists():
            ProtocolLabelList = []
            ProtocolLabelList.append(ProtocolLabel(name = "Request", desc = "客户端发起请求"))
            ProtocolLabelList.append(ProtocolLabel(name = "Response", desc = "服务器根据客户端发起的一对一的回复"))
            ProtocolLabelList.append(ProtocolLabel(name = "Notification", desc = "服务器单方面通知客户端的消息"))
            ProtocolLabel.objects.bulk_create(ProtocolLabelList)

        if not FieldType.objects.exists():
            FieldTypeList = []
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 1, typename = "double", desc = "双精度浮点数"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 2, typename = "float", desc = "单精度浮点数"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 3, typename = "int64", desc = "64位整形"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 4, typename = "uint64", desc = "无符号64位整形"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 5, typename = "int32", desc = "32位整形"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 6, typename = "fixed64", desc = "64位无符号整形，打包效率高，内存大"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 7, typename = "fixed32", desc = "32位无符号整形，打包效率高，内存大"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 8, typename = "bool", desc = "布尔类型"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 9, typename = "string", desc = "A string must always contain UTF-8 encoded or 7-bit ASCII text."))
            # FieldTypeList.append(FieldType(module = None, type = 10, typename = "group"))
            # FieldTypeList.append(FieldType(module = None, type = 11, typename = "message"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 12, typename = "bytes", desc = "May contain any arbitrary sequence of bytes."))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 13, typename = "uint32", desc = "无符号32位整形"))
            # FieldTypeList.append(FieldType(module = None, type = 14, typename = "enum"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 15, typename = "sfixed32", desc = "32位整形，处理负数效率高，打包快内存大。"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 16, typename = "sfixed64", desc = "64位整形，处理负数效率高，打包快内存大。"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 17, typename = "sint32", desc = "32位整形，处理负数的效率更高"))
            FieldTypeList.append(FieldType(module = None, priority = 0, type = 18, typename = "sint64", desc = "64位整形，处理负数效率更高"))
            FieldType.objects.bulk_create(FieldTypeList)

 
post_migrate.connect(init_db)
