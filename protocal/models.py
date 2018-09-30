# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Lock(models.Model):
	lock_owner = models.CharField(max_length = 150, black = False)
	lock_timestamp = models.DateTimeField(auto_now_add = True)

class Project(models.Model):
	title = models.CharField(max_length = 150, black = False)
	namespace = models.CharField(max_length = 150, blank = False, unique = True)
	timestamp = models.DateTimeField(auto_now_add = True)
	def __unicode__(self):
		return self.title

class ProjectBranche(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    title = models.CharField(max_length = 150, black = False)
	proto_url = models.CharField(max_length = 150, black = False)
	timestamp = models.DateTimeField(auto_now_add = True)
	def __unicode__(self):
		return self.title

class Module(models.Model):
    project = models.ForeignKey(ProjectBranche, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100,blank = False)
    fullname = models.CharField(max_length = 100, blank = False)
    desc = models.CharField(max_length = 150,blank = False)
    def __unicode__(self):
        return self.name

class Protocal(models.Model):
    module = models.ForeignKey(Module, on_delete = models.CASCADE, null = True, default = None)
    name = models.CharField(max_length = 100, blank = False)
    fullname = models.CharField(max_length = 100, blank = False)
    desc = models.CharField(max_length = 150, blank = False)
    nested = models.ForeignKey(Protocal, null = True, default = None)
    timestamp = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.name

class SegmentLabel(models.Model):
    name = models.CharField(max_length = 100, blank = False)
    desc = models.CharField(max_length = 150, blank = False)
    def __unicode__(self):
        return self.name

class SegmentType(models.Model):
	type = models.IntegerField()
	

class Segment(models.Model):
    protocal = models.ForeignKey(Protocal, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, blank = False)
    fullname = models.CharField(max_length = 100, blank = False)
    desc = models.CharField(max_length = 150, blank = False)
    label = models.ForeignKey(SegmentLabel)
    number = models.IntegerField()
    type = 
    def __unicode__(self):
        return self.name
