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

import utils
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

        lock = Lock.objects.first()
        if lock:
            raise Exception('Project is Locking.Wait until locking done')

        export_version = request.POST['export_version']
        export_history = ExportHistory(project=cur_branch, version=export_version, status=1)
        export_history.save()

        lock = Lock(lock_owner="export_" + cur_branch.title)
        lock.save()
        try:
            helper.exporter(cur_branch.project, cur_branch)
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
        context['message'] = Message.objects.filter(module__in=modules).order_by('-timestamp')
        context['sugget_version'] = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        context['history_list'] = ExportHistory.objects.filter(project=cur_branch).order_by('-timestamp')[:10]
        return render(request, 'branch_export.html', context)


def branch_sync(request, branch_id):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    if request.method == 'POST':

        lock = Lock.objects.first()
        if lock:
            raise Exception('Project is Locking.Wait until locking done')

        sync_history = SyncHistory(project=cur_branch, status=1)
        sync_history.save()

        lock = Lock(lock_owner="sync_proto_"+cur_branch.title)
        lock.save()
        try:
            helper.syncer(cur_branch.project, cur_branch)
            sync_history.status = 2
            sync_history.save(update_fields=['status'])
        except Exception, e:
            sync_history.status = 3
            sync_history.save(update_fields=['status'])
            raise e
        finally:
            lock.delete()

        return HttpResponse("<h1>Sync successfully .</h1>")
    else:
        context = {}
        context['cur_branch'] = cur_branch
        modules = Module.objects.filter(project=cur_branch)
        context['modules'] = modules
        context['need_update'] = helper.testSync(cur_branch.project, cur_branch)
        context['message'] = Message.objects.filter(module__in=modules).order_by('-timestamp')
        context['history_list'] = SyncHistory.objects.filter(project=cur_branch).order_by('-timestamp')[:10]
        return render(request, 'branch_sync.html', context)


def protocol_detail(request, branch_id, protocol_key):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    cur_message = get_object_or_404(Message, module__project=cur_branch, fullname=protocol_key)
    cur_protocol = get_object_or_404(Protocol, message=cur_message)
    cur_module = cur_message.module
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


def message_detail(request, branch_id, message_key):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    cur_message = get_object_or_404(Message, module__project=cur_branch, fullname=message_key)
    cur_module = cur_message.module
    fields = Field.objects.filter(message=cur_message).order_by('number')
    return render(
        request, 'message_detail_dialog.html', {
            'cur_branch': cur_branch,
            'cur_module': cur_module,
            'cur_message': cur_message,
            'fields': fields,
        })


def enum_detail(request, branch_id, enum_key):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    pass


def module_detail(request, branch_id, module_id):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    if utils.try_parse_int(module_id) == 0:
        modules = Module.objects.filter(project=cur_branch)
        messages = Message.objects.filter(module__project=cur_branch)
        enums = Enum.objects.filter(module__project=cur_branch)
        protocols = Protocol.objects.filter(message__in=messages).order_by('protocol_id')

        return render(request, 'branch_detail.html', {
            'cur_branch': cur_branch,
            'modules': modules,
            'protocols': protocols,
            'messages': messages.exclude(pk__in=protocols.values_list('message')),
            'enums': enums,
        })
    else:
        cur_module = get_object_or_404(Module, pk=module_id)
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

