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
import base64

def do_branch_export(cur_branch, version):
    lock = Lock.objects.first()
    if lock:
        raise Exception('Project is Locking.Wait until locking done')

    export_version = version
    export_history = ExportHistory(project=cur_branch, version=export_version, status=1)
    export_history.save()

    lock = Lock(lock_owner="export_" + cur_branch.title)
    lock.save()
    try:
        helper.exporter(cur_branch.project, cur_branch, export_history, export_version)
        export_history.status = 2
        export_history.save(update_fields=['status'])
    except Exception, e:
        export_history.status = 3
        export_history.save(update_fields=['status'])
        raise e
    finally:
        lock.delete()

def do_branch_sync(cur_branch, bForce):
    lock = Lock.objects.first()
    if lock:
        raise Exception('Project is Locking.Wait until locking done')

    sync_history = SyncHistory(project=cur_branch, status=1)
    sync_history.save()

    lock = Lock(lock_owner="sync_proto_"+cur_branch.title)
    lock.save()
    try:
        helper.syncer(cur_branch.project, cur_branch, sync_history, bForce)
        sync_history.status = 2
        sync_history.save(update_fields=['status'])
    except Exception, e:
        sync_history.status = 3
        sync_history.save(update_fields=['status'])
        raise e
    finally:
        lock.delete()

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

def download_proto(request, url_string):
    if request.method == 'GET':
        realUrl = base64.b64decode(url_string)
        print("download ", realUrl)

        branch_id = -1
        for branch in ProjectBranch.objects.all():
            fullUrl = branch.project.urlbase + branch.proto_url
            fullUrl = fullUrl.lower()
            if fullUrl.find(realUrl.lower()) >= 0:
                branch_id = branch.pk
                break

        cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
        the_file_path = helper.zipExporter(cur_branch.project, cur_branch)
        the_file_name = os.path.basename(the_file_path)

        def file_iterator(file_path, chunk_size=512):
            with open(file_path,'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        file_size = os.path.getsize(the_file_path)
        print 'file size:' + str(file_size)
        response = StreamingHttpResponse(file_iterator(the_file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        response['Content-Length'] = file_size
        return response

    else:
        return HttpResponse("<h1>Invalid request.</h1>")


def export_download_proto(request, url_string):
    if request.method == 'GET':
        realUrl = base64.b64decode(url_string)
        print("download ", realUrl)

        branch_id = -1
        for branch in ProjectBranch.objects.all():
            fullUrl = branch.project.urlbase + branch.proto_url
            fullUrl = fullUrl.lower()
            if fullUrl.find(realUrl.lower()) >= 0:
                branch_id = branch.pk
                break

        cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)

        do_branch_sync(cur_branch, True)
        do_branch_export(cur_branch, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

        the_file_path = helper.zipExporter(cur_branch.project, cur_branch)
        the_file_name = os.path.basename(the_file_path)

        def file_iterator(file_path, chunk_size=512):
            with open(file_path,'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        file_size = os.path.getsize(the_file_path)
        print 'file size:' + str(file_size)
        response = StreamingHttpResponse(file_iterator(the_file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        response['Content-Length'] = file_size
        return response

    else:
        return HttpResponse("<h1>Invalid request.</h1>")

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
        try:
            do_branch_export(cur_branch, request.POST['export_version'])
        except Exception, e:
            raise e

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
        try:
            do_branch_sync(cur_branch, False)
        except Exception, e:
            raise e

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

def branch_force_sync(request, branch_id):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    if request.method == 'POST':
        try:
            do_branch_sync(cur_branch, True)
        except Exception, e:
            raise e

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
    fields = Field.objects.filter(message=cur_message).order_by('number')

    childmessages = Message.objects.filter(nested=cur_message)
    if len(childmessages) > 0:
        cur_protocol.childmessages = childmessages
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
    
    childmessages = Message.objects.filter(nested=cur_message)
    if len(childmessages) > 0:
        cur_message.childmessages = childmessages

    return render(
        request, 'message_detail_dialog.html', {
            'cur_branch': cur_branch,
            'cur_module': cur_module,
            'cur_message': cur_message,
            'fields': fields,
        })


def enum_detail(request, branch_id, enum_key):
    print(branch_id, enum_key)
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    cur_enum = get_object_or_404(Enum, module__project=cur_branch, fullname=enum_key)
    cur_module = cur_enum.module
    values = EnumValue.objects.filter(enum=cur_enum).order_by('number')

    return render(
        request, 'enum_detail_dialog.html', {
            'cur_branch': cur_branch,
            'cur_module': cur_module,
            'cur_enum': cur_enum,
            'values': values,
        })


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
            'messages': messages.exclude(pk__in=protocols.values_list('message')).order_by('name'),
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
            'messages': messages.exclude(pk__in=protocols.values_list('message')).order_by('name'),
            'enums': enums,
        })


def branch_download(request, branch_id):
    cur_branch = get_object_or_404(ProjectBranch, pk=branch_id)
    the_file_path = helper.zipExporter(cur_branch.project, cur_branch)
    the_file_name = os.path.basename(the_file_path)

    def file_iterator(file_path, chunk_size=512):
        with open(file_path,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    file_size = os.path.getsize(the_file_path)
    print 'file size:' + str(file_size)
    response = StreamingHttpResponse(file_iterator(the_file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    response['Content-Length'] = file_size
    return response
