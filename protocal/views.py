# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import os
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.forms.models import ModelForm
from django.http.response import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext  

from datetime import datetime
from string import strip

from protocal.models import *

# Create your views here.

def index(request):
	raw_projects = Project.objects.all().order_by('-timestamp')
	projects = []
	for project in raw_projects:
		projects.append({
			'project' : project,
			'branches' : ProjectBranche.objects.all().filter(project = project)
		})		
	return render(request, 'index.html', {'projects' : projects})


def project_create(request):
	if request.method == 'POST': 
		project_name = request.POST['project_name'] 
		project_namespace = request.POST['project_namespace'] 
		
		if project_name and project_namespace:
			project = Project(title = strip(project_name), namespace = strip(project_namespace))
			project.save()
		else:
			raise ValidationError("name or namespace should not be null.")

		return HttpResponse("<h1>Created successfully .</h1>")  
	else:
		return HttpResponse("<h1>Invalid request.</h1>")  

def project_create_branche(request):
	if request.method == 'POST': 
		project_id = request.POST['project_id']
		branche_title = request.POST['branche_title'] 
		branche_url = request.POST['branche_url'] 

		project = Project.objects.get(id = project_id)

		if project_id and branche_title and branche_url:
			project = ProjectBranche(project = project, title = strip(branche_title), proto_url = strip(branche_url))
			project.save()
		else:
			raise ValidationError("id or name or url should not be null.")

		return HttpResponse("<h1>Created successfully .</h1>")  
	else:
		return HttpResponse("<h1>Invalid request.</h1>")  


def project_detail(request, project_id):
	return HttpResponse("Hello， World!")