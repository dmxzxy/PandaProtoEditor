from django import template
register = template.Library()


@register.filter(name='segtype_a')
def segtype_a(field_type):

    names = field_type.typename.split('.')
    field_type_name = names[len(names) - 1]


    if field_type.type == 11:
        branch = field_type.module.project
        return "<a class='show_child_message_detail' id='%s' val='%s' title='%s'>%s</a>" % (
            field_type.typename, branch.id, field_type_name, field_type_name)
    elif field_type.type == 14:
        branch = field_type.module.project
        return "<a class='show_child_enum_detail' id='%s' val='%s' title='%s'>%s</a>" % (
            field_type.typename, branch.id, field_type_name, field_type_name)
    elif field_type.type == 10:
        return "group"
    else:
        return field_type_name


@register.filter(name='segtype')
def segtype(field):
    # if field.type.name == 'map':
    #     return 'map&lt;' + segtype_a(segment.extra_type1) + ',' + segtype_a(segment.extra_type2) + '&gt;'
    return segtype_a(field.type)