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

from export_tool import export_center
from sync_tool import sync_proto_helper

import project_helper

# Create your views here.


def index(request):
    raw_projects = Project.objects.all().order_by('-timestamp')
    projects = []
    for project in raw_projects:
        projects.append({
            'project':
            project,
            'branches':
            ProjectBranche.objects.all().filter(project=project)
        })
    return render(request, 'index.html', {'projects': projects})


def project_create(request):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        project_namespace = request.POST['project_namespace']

        if project_name and project_namespace:
            project_helper.do_make_project(project_name, project_namespace)
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

        if project_id and branche_title and branche_url:
            project_helper.do_make_branche(project_id, branche_title,
                                           branche_url)
        else:
            raise ValidationError("id or name or url should not be null.")

        return HttpResponse("<h1>Created successfully .</h1>")
    else:
        return HttpResponse("<h1>Invalid request.</h1>")


def branche_detail(request, branche_id):
    cur_branche = get_object_or_404(ProjectBranche, pk=branche_id)
    modules = Module.objects.filter(project=cur_branche)

    messages = Message.objects.filter(module__in=modules)
    enums = Enum.objects.filter(module__in=modules)
    protocals = Protocal.objects.filter(message__in=messages).order_by('protocal_id')

    return render(request, 'branche_detail.html', {
        'cur_branche': cur_branche,
        'modules': modules,
        'protocals': protocals,
        'messages': messages,
        'enums': enums,
    })


def branche_help(request, branche_id):
    cur_branche = get_object_or_404(ProjectBranche, pk=branche_id)
    modules = Module.objects.filter(project=cur_branche)
    messages = Message.objects.filter(
        module__in=modules).order_by('-timestamp')
    protocal_labels = ProtocalLabel.objects.all()
    return render(
        request, 'project_help.html', {
            'cur_branche': cur_branche,
            'modules': modules,
            'messages': messages,
            'protocal_labels': protocal_labels,
        })


def branche_export(request, branche_id):
    cur_branche = get_object_or_404(ProjectBranche, pk=branche_id)
    if request.method == 'POST':
        export_version = request.POST['export_version']
        export_history = ExportHistory(
            project=cur_branche, version=export_version, status=1)

        lock = Lock.objects.first()

        if lock:
            raise Exception('Project is Locking.Wait until locking done')

        export_history.save()

        lock = Lock(lock_owner="export_" + cur_branche)
        export_setting = ExportSetting.objects.first()
        try:
            export_center.do_export(cur_branche.project, cur_branche,
                                    export_version, export_setting)
            export_history.status = 2
            export_history.save(update_fields=['status'])
        except Exception, e:
            export_history.status = 3
            export_history.save(update_fields=['status'])
            raise e
        finally:
            lock.delete()

        return HttpResponse("<h1>Export successfully .</h1>")
    else:
        context = {}
        context['cur_branche'] = cur_branche
        modules = Module.objects.filter(project=cur_branche)
        context['modules'] = modules
        context['message'] = Message.objects.filter(
            module__in=modules).order_by('-timestamp')
        context['sugget_version'] = datetime.now().strftime(
            '%Y-%m-%d-%H-%M-%S')
        return render(request, 'branche_export.html', context)


def branche_sync(request, branche_id):
    cur_branche = get_object_or_404(ProjectBranche, pk=branche_id)
    if request.method == 'POST':

        # lock = Lock.objects.first()
        # if lock:
        #     raise Exception('Project is Locking.Wait until locking done')

        # lock = Lock(lock_owner="sync_proto_"+cur_branche)
        try:
            sync_proto_helper.sync(cur_branche.project, cur_branche)
        except Exception, e:
            raise e
        finally:
            pass
        # lock.delete()

        return HttpResponse("<h1>Sync successfully .</h1>")
    else:
        context = {}
        context['cur_branche'] = cur_branche
        modules = Module.objects.filter(project=cur_branche)
        context['modules'] = modules
        context['message'] = Message.objects.filter(
            module__in=modules).order_by('-timestamp')
        context["need_update"] = True
        return render(request, 'branche_sync.html', context)


def protocal_detail(request, protocal_key):
    cur_message = get_object_or_404(Message, fullname=protocal_key)
    cur_protocal = get_object_or_404(Protocal, message=cur_message)
    cur_module = cur_message.module
    cur_branche = cur_module.project
    # innerEnums = Enum.objects.filter(belong=cur_protocal)
    # innerCustomTypes = CustomType.objects.filter(belong=cur_protocal)
    # if len(innerEnums) > 0:
    #     cur_protocal.innerEnums = innerEnums
    # if len(innerCustomTypes) > 0:
    #     cur_protocal.innerCustomTypes = innerCustomTypes
    # segments = Segment.objects.filter(protocal=cur_protocal)

    # cur_protocal_ext = ProtocalExtension.objects.get(
    #     protocal_id=cur_protocal.protocal_id)
    # cur_protocal.type = cur_protocal_ext.protocal_type
    fields = Field.objects.filter(message=cur_message).order_by('number')
    return render(
        request, 'protocal_detail_dialog.html', {
            'cur_branche': cur_branche,
            'cur_module': cur_module,
            'cur_protocal': cur_protocal,
            'fields': fields,
        })


def message_detail(request, message_key):
    cur_message = get_object_or_404(Message, fullname=message_key)
    cur_module = cur_message.module
    cur_branche = cur_module.project
    fields = Field.objects.filter(message=cur_message).order_by('number')
    return render(
        request, 'message_detail_dialog.html', {
            'cur_branche': cur_branche,
            'cur_module': cur_module,
            'cur_message': cur_message,
            'fields': fields,
        })


def enum_detail(request, enum_key):
    pass


def module_detail(request, module_id):
    cur_module = get_object_or_404(Module, pk=module_id)
    cur_branche = cur_module.project

    modules = Module.objects.filter(project=cur_branche)
    messages = Message.objects.filter(module=cur_module)
    enums = Enum.objects.filter(module=cur_module)
    protocals = Protocal.objects.filter(message__in=messages).order_by('protocal_id')

    return render(request, 'branche_detail.html', {
        'cur_branche': cur_branche,
        'modules': modules,
        'protocals': protocals,
        'messages': messages,
        'enums': enums,
    })

