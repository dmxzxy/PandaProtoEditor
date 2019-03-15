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

from protocol.models import *

from protocol.helpers import helper
from protocol.helpers import projecthelper

# Create your views here.
def index(request):
    raw_projects = Project.objects.all().order_by('-timestamp')
    projects = []
    for project in raw_projects:
        projects.append({
            'project':project,
            'branchs':ProjectBranch.objects.all().filter(project=project)
        })
    return render(request, 'index.html', {'projects': projects})


def project_create(request):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        project_namespace = request.POST['project_namespace']
        project_svnurlbase = request.POST['project_svnurlbase']

        if project_name and project_namespace:
            projecthelper.do_make_project(project_name, project_namespace, project_svnurlbase)
        else:
            raise ValidationError("name or namespace should not be null.")

        return HttpResponse("<h1>Created successfully .</h1>")
    else:
        return HttpResponse("<h1>Invalid request.</h1>")


def project_create_branch(request):
    if request.method == 'POST':
        project_id = request.POST['project_id']
        branch_title = request.POST['branch_title']
        branch_url = request.POST['branch_url']

        if project_id and branch_title and branch_url:
            projecthelper.do_make_branch(project_id, branch_title, branch_url)
        else:
            raise ValidationError("id or name or url should not be null.")

        return HttpResponse("<h1>Created successfully .</h1>")
    else:
        return HttpResponse("<h1>Invalid request.</h1>")


def branch_detail(request, branch_id):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    modules = Module.objects.filter(project=cur_branch)

    messages = Message.objects.filter(module__in=modules)
    enums = Enum.objects.filter(module__in=modules)
    protocols = Protocol.objects.filter(message__in=messages).order_by('protocol_id')

    return render(request, 'branch_detail.html', {
        'cur_branch': cur_branch,
        'modules': modules,
        'protocols': protocols,
        'messages': messages,
        'enums': enums,
    })


def branch_help(request, branch_id):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    modules = Module.objects.filter(project=cur_branch)
    messages = Message.objects.filter(
        module__in=modules).order_by('-timestamp')
    protocol_labels = ProtocolLabel.objects.all()
    return render(
        request, 'project_help.html', {
            'cur_branch': cur_branch,
            'modules': modules,
            'messages': messages,
            'protocol_labels': protocol_labels,
        })


def branch_export(request, branch_id):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    if request.method == 'POST':
        export_version = request.POST['export_version']
        export_history = ExportHistory(
            project=cur_branch, version=export_version, status=1)

        lock = Lock.objects.first()

        if lock:
            raise Exception('Project is Locking.Wait until locking done')

        export_history.save()

        lock = Lock(lock_owner="export_" + cur_branch)
        export_setting = ExportSetting.objects.first()
        try:
            # export_center.do_export(cur_branch.project, cur_branch,
            #                         export_version, export_setting)
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
        context['cur_branch'] = cur_branch
        modules = Module.objects.filter(project=cur_branch)
        context['modules'] = modules
        context['message'] = Message.objects.filter(
            module__in=modules).order_by('-timestamp')
        context['sugget_version'] = datetime.now().strftime(
            '%Y-%m-%d-%H-%M-%S')
        return render(request, 'branch_export.html', context)


def branch_sync(request, branch_id):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    if request.method == 'POST':

        # lock = Lock.objects.first()
        # if lock:
        #     raise Exception('Project is Locking.Wait until locking done')

        # lock = Lock(lock_owner="sync_proto_"+cur_branch)
        try:
            helper.syncer(cur_branch.project, cur_branch)
        except Exception, e:
            raise e
        finally:
            pass
        # lock.delete()

        return HttpResponse("<h1>Sync successfully .</h1>")
    else:
        context = {}
        context['cur_branch'] = cur_branch
        modules = Module.objects.filter(project=cur_branch)
        context['modules'] = modules
        context['message'] = Message.objects.filter(
            module__in=modules).order_by('-timestamp')
        context["need_update"] = True
        return render(request, 'branch_sync.html', context)


def protocol_detail(request, protocol_key):
    cur_message = get_object_or_404(Message, fullname=protocol_key)
    cur_protocol = get_object_or_404(Protocol, message=cur_message)
    cur_module = cur_message.module
    cur_branch = cur_module.project
    # innerEnums = Enum.objects.filter(belong=cur_protocol)
    # innerCustomTypes = CustomType.objects.filter(belong=cur_protocol)
    # if len(innerEnums) > 0:
    #     cur_protocol.innerEnums = innerEnums
    # if len(innerCustomTypes) > 0:
    #     cur_protocol.innerCustomTypes = innerCustomTypes
    # segments = Segment.objects.filter(protocol=cur_protocol)

    # cur_protocol_ext = protocolExtension.objects.get(
    #     protocol_id=cur_protocol.protocol_id)
    # cur_protocol.type = cur_protocol_ext.protocol_type
    fields = Field.objects.filter(message=cur_message).order_by('number')
    return render(
        request, 'protocol_detail_dialog.html', {
            'cur_branch': cur_branch,
            'cur_module': cur_module,
            'cur_protocol': cur_protocol,
            'fields': fields,
        })


def message_detail(request, message_key):
    cur_message = get_object_or_404(Message, fullname=message_key)
    cur_module = cur_message.module
    cur_branch = cur_module.project
    fields = Field.objects.filter(message=cur_message).order_by('number')
    return render(
        request, 'message_detail_dialog.html', {
            'cur_branch': cur_branch,
            'cur_module': cur_module,
            'cur_message': cur_message,
            'fields': fields,
        })


def enum_detail(request, enum_key):
    pass


def module_detail(request, module_id):
    cur_module = get_object_or_404(Module, pk=module_id)
    cur_branch = cur_module.project
    modules = Module.objects.filter(project=cur_branch)
    messages = Message.objects.filter(module=cur_module)
    enums = Enum.objects.filter(module=cur_module)
    protocols = Protocol.objects.filter(message__in=messages).order_by('protocol_id')

    return render(request, 'branch_detail.html', {
        'cur_branch': cur_branch,
        'cur_module': cur_module,
        'modules': modules,
        'protocols': protocols,
        'messages': messages,
        'enums': enums,
    })

