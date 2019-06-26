# -*- coding: utf-8 -*-

import os
from string import strip

from django.conf import settings

from protocol.models import Project
from protocol.models import ProjectBranch
from django.shortcuts import get_object_or_404


def _get_temp_path():
    temp_path = os.path.join(settings.BASE_DIR, 'temp')
    return temp_path + '/'


def _check_temp_path():
    temp_path = _get_temp_path()

    if not os.path.exists(temp_path):
        os.mkdir(temp_path)


def do_make_project(title, namespace, urlbase):
    project = Project(title=strip(title), namespace=strip(namespace), urlbase=strip(urlbase))
    project.save()

    _check_temp_path()

    project_path = _get_temp_path() + project.title + '/'
    if not os.path.exists(project_path):
        os.mkdir(project_path)


def do_make_branch(project_id, title, url):
    project = get_object_or_404(Project, pk=project_id)

    branch = ProjectBranch(
        project=project, title=strip(title), proto_url=strip(url))
    branch.save()

    _check_temp_path()

    branch_path = _get_temp_path() + project.title + '/' + branch.title + '/'

    if not os.path.exists(branch_path):
        os.mkdir(branch_path)


def get_branch_path(branch_id):
    branch = get_object_or_404(ProjectBranch, pk=branch_id)
    project = branch.project
    branch_path = _get_temp_path() + project.title + '/' + branch.title + '/'
    return branch_path

def get_branch_log_path(branch_id):
    branch = get_object_or_404(ProjectBranch, pk=branch_id)
    project = branch.project
    branch_log_path = _get_temp_path() + project.title + '/' + branch.title + '/log/'
    return branch_log_path