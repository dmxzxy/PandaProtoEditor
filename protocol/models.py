# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Lock(models.Model):
	lock_owner = models.CharField(max_length = 150, blank = False)
	lock_timestamp = models.DateTimeField(auto_now_add = True)

# optional required repeated 这是proto2的基本label类型
class FieldLabel(models.Model):
    name = models.CharField(max_length = 100, blank = False)
    desc = models.CharField(max_length = 150, blank = False)
    def __unicode__(self):
        return self.name

# Request 客户端发起请求
# Response 服务器根据客户端发起的一对一的回复
# Notification 服务器单方面通知客户端的消息
class ProtocolLabel(models.Model):
    name = models.CharField(max_length = 100,blank = False, unique = True)
    desc = models.CharField(max_length = 150,blank = False)
    def __unicode__(self):
        return self.name

#---------------------------------------------------------------------------------
#         
class Project(models.Model):
    title = models.CharField(max_length = 150, blank = False)
    namespace = models.CharField(max_length = 150, blank = False, unique = True)
    urlbase = models.CharField(max_length = 150, blank = False)
    timestamp = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
		return self.title

class ProjectBranch(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    title = models.CharField(max_length = 150, blank = False)
    proto_url = models.CharField(max_length = 150, blank = False)
    timestamp = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.title

class Module(models.Model):
    project = models.ForeignKey(ProjectBranch, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100,blank = False)
    fullname = models.CharField(max_length = 100, blank = False)
    desc = models.CharField(max_length = 150,blank = False)
    def __unicode__(self):
        return self


#// 0 is reserved for errors.
#// Order is weird for historical reasons.
#TYPE_DOUBLE         = 1;
#TYPE_FLOAT          = 2;
#// Not ZigZag encoded.  Negative numbers take 10 bytes.  Use TYPE_SINT64 if
#// negative values are likely.
#TYPE_INT64          = 3;
#TYPE_UINT64         = 4;
#// Not ZigZag encoded.  Negative numbers take 10 bytes.  Use TYPE_SINT32 if
#// negative values are likely.
#TYPE_INT32          = 5;
#TYPE_FIXED64        = 6;
#TYPE_FIXED32        = 7;
#TYPE_BOOL           = 8;
#TYPE_STRING         = 9;
#TYPE_GROUP          = 10;  // Tag-delimited aggregate.
#TYPE_MESSAGE        = 11;  // Length-delimited aggregate.

# New in version 2.
#TYPE_BYTES          = 12;
#TYPE_UINT32         = 13;
#TYPE_ENUM           = 14;
#TYPE_SFIXED32       = 15;
#TYPE_SFIXED64       = 16;
#TYPE_SINT32         = 17;  // Uses ZigZag encoding.
#TYPE_SINT64         = 18;  // Uses ZigZag encoding

class FieldType(models.Model):
    module = models.ForeignKey(Module, on_delete = models.CASCADE, null = True, default = None)
    type = models.IntegerField()
    typename = models.CharField(max_length = 150)
    desc = models.CharField(max_length = 150, blank = False)
    priority = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.typename

class Message(models.Model):
    module = models.ForeignKey(Module, on_delete = models.CASCADE, null = True, default = None)
    name = models.CharField(max_length = 100, blank = False)
    fullname = models.CharField(max_length = 100, blank = False)
    desc = models.CharField(max_length = 150, blank = False)
    nested = models.ForeignKey("Message", null = True, default = None)
    timestamp = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.name

class Field(models.Model):
    message = models.ForeignKey(Message, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, blank = False)
    fullname = models.CharField(max_length = 150, blank = False)
    desc = models.CharField(max_length = 150, blank = False)
    label = models.ForeignKey(FieldLabel)
    type = models.ForeignKey(FieldType)
    number = models.IntegerField()
    def __unicode__(self):
        return self.name

class Enum(models.Model):
    module = models.ForeignKey(Module, on_delete = models.CASCADE, null = True, default = None)
    name = models.CharField(max_length = 100, blank = False)
    fullname = models.CharField(max_length = 150, blank = False)
    desc = models.CharField(max_length = 150, blank = False)
    nested = models.ForeignKey("Message", null = True, default = None)
    timestamp = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.name

class EnumValue(models.Model):
    enum = models.ForeignKey(Enum, on_delete = models.CASCADE, null = True, default = None)
    name = models.CharField(max_length = 100, blank = False)
    fullname = models.CharField(max_length = 150, blank = False)
    desc = models.CharField(max_length = 150, blank = False)
    number = models.IntegerField()
    def __unicode__(self):
        return self.name

class Protocol(models.Model):
    message = models.OneToOneField(Message, on_delete = models.CASCADE)
    protocol_id = models.IntegerField()
    protocol_ref = models.ForeignKey("Protocol", null = True)
    protocol_label = models.ForeignKey(ProtocolLabel)
    timestamp = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.protocol_id

#---------------------------------------------------------


class ExportHistory(models.Model):
    project = models.ForeignKey(ProjectBranch, on_delete = models.CASCADE)
    version = models.CharField(max_length = 100)
    Export_Status = (
        (1, "Executing"),
        (2, "Successfully"),
        (3, "Failed"),
    )
    status = models.IntegerField(choices = Export_Status, default = 1)
    timestamp = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.version


class ExportSetting(models.Model):
    project = models.ForeignKey(ProjectBranch, on_delete = models.CASCADE)
    export_path = models.CharField(max_length = 300, blank = False)
    def __unicode__(self):
        return self.export_path  


class SyncHistory(models.Model):
    project = models.ForeignKey(ProjectBranch, on_delete = models.CASCADE)
    Sync_Status = (
        (1, "Executing"),
        (2, "Successfully"),
        (3, "Failed"),
    )
    status = models.IntegerField(choices = Sync_Status, default = 1)
    timestamp = models.DateTimeField(auto_now_add = True)
