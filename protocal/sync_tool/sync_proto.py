
from string import strip
from protocal.models import *

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


def do_sync(context):
    cur_branche = context.branche
    proto_parse_dict = context.proto_parse_dict
    project_namespace = context.project.namespace
    ModuleList = []
    for module_dict in proto_parse_dict['modulelist']:
        module_namespace = module_dict['package']
        if project_namespace == module_namespace:
            pass
        else:
            module_modulename = module_namespace.replace(
                project_namespace + '.', '')
            module_name = module_modulename
            module_desc = module_modulename
            ModuleList.append(
                Module(
                    project=cur_branche,
                    name=module_modulename,
                    fullname=strip(module_name),
                    desc=module_desc,
                ))
    Module.objects.bulk_create(ModuleList)

    pass
