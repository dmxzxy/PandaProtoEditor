#!/usr/bin/env python
# -*- encoding:utf8 -*-

from protocol.models import ProtocolLabel
from protocol.models import ProjectBranch
from protocol.models import FieldLabel
from protocol.models import FieldType
from protocol.models import Message
from protocol.models import Protocol
from protocol.models import Module
from protocol.models import Field

from protocol.helpers.panpbtool.data import middata
from protocol.helpers.panpbtool.conf import prototype

class translater():
    branch = None
    project_data = None

    def __translate_field(self, belong, field):
        location = "field_"+field.fullname
        belong.add_field(
            name = field.name, 
            fullname = field.fullname,
            namespace = belong.fullname,
            proto_type = middata.ProtocolType(field.type.type, field.type.typename, prototype.get_is_basic(field.type.type)),
            label = field.label.id,
            number = field.number,
            location = location
        )
        project_data = self.project_data
        project_data.add_comment(location, field.desc)

    def __translate_message(self, belong, message, isproto):
        project_data = self.project_data
        if isproto:
            location = "message_"+message.message.fullname
            message_data = belong.add_protocol(
                id = message.protocol_id,
                category = message.protocol_label.name,
                name = message.message.name,
                fullname = message.message.fullname,
                namespace = belong.fullname,
                location = location
            )
            project_data.add_comment(location, message.message.desc)
            fields = Field.objects.filter(message=message.message)
            for field in fields:
                self.__translate_field(message_data, field)

            messages = Message.objects.filter(nested=message.message)
            for msg in messages:
                self.__translate_message(message_data, msg, False)
        else:
            if message.nested == None or message.nested.fullname == belong.fullname:
                location = "message_"+message.fullname
                message_data = belong.add_message(
                    name = message.name,
                    fullname = message.fullname,
                    namespace = belong.fullname,
                    location = location
                )
                project_data.add_comment(location, message.desc)
                fields = Field.objects.filter(message=message)
                for field in fields:
                    self.__translate_field(message_data, field)

                messages = Message.objects.filter(nested=message)
                for msg in messages:
                    self.__translate_message(message_data, msg, False)
        
    def __translate_module(self, module):
        project_data = self.project_data
        location = "module_"+module.fullname
        module_data = project_data.add_module(
            name = module.name,
            fullname = module.fullname,
            namespace = self.branch.project.namespace,
            location = location
        )
        project_data.add_comment(location, module.desc)

        messages = Message.objects.filter(module__project=self.branch)
        protocols = Protocol.objects.filter(message__in=messages)
        messages = messages.exclude(pk__in=protocols.values_list('message'))

        for message in messages:
            self.__translate_message(module_data, message, False)
        
        for protocol in protocols:
            self.__translate_message(module_data, protocol, True)

    def translate(self, branch):
        self.branch = branch

        project_data = middata.Project()
        self.project_data = project_data

        modules = Module.objects.filter(project = branch)
        for module in modules:
            self.__translate_module(module)

        return project_data


def translate(branch):
    worker = translater()
    return worker.translate(branch)