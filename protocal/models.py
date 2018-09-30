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
