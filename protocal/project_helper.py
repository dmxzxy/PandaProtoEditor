# -*- coding: utf-8 -*-

import os
from string import strip

from django.conf import settings

from protocal.models import Project
from protocal.models import ProjectBranche
from django.shortcuts import get_object_or_404


def _get_temp_path():
    temp_path = os.path.join(settings.BASE_DIR, 'temp')
    return temp_path + '/'


def _check_temp_path():
    temp_path = _get_temp_path()

    if not os.path.exists(temp_path):
        os.mkdir(temp_path)


def do_make_project(title, namespace):
    project = Project(title=strip(title), namespace=strip(namespace))
    project.save()

    _check_temp_path()

    project_path = _get_temp_path() + project.title + '/'
    if not os.path.exists(project_path):
        os.mkdir(project_path)


def do_make_branche(project_id, title, url):
    project = get_object_or_404(Project, pk=project_id)

    branche = ProjectBranche(
        project=project, title=strip(title), proto_url=strip(url))
    branche.save()

    _check_temp_path()

    branche_path = _get_temp_path() + project.title + '/' + branche.title + '/'

    if not os.path.exists(branche_path):
        os.mkdir(branche_path)


def get_branche_path(branche_id):
    branche = get_object_or_404(ProjectBranche, pk=branche_id)
    project = branche.project
    branche_path = _get_temp_path() + project.title + '/' + branche.title + '/'
    return branche_path
