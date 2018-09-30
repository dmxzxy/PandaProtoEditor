# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def index(request):
	projects = Project.objects.all().order_by('-timestamp')
	return render(request, 'index.html',{'projects' : projects})
