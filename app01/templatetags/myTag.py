from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def list_distinct(course_module,name):
    str = ""
    # print(name)
    # count=0
    if name == "c":
        temp = []
        str += "<option %s>%s</option>" % ("selected", "---------")
        for c_m in course_module:
            if not c_m.c_id.id in temp:
                temp.append(c_m.c_id.id)
                str += "<option value='%s'>%s</option>" % (c_m.c_id.id, c_m.c_id.name)
    elif name == "m":
        temp = []
        str += "<option %s>%s</option>" % ("selected", "---------")
        for c_m in course_module:
            if not c_m.m_id.id in temp:
                temp.append(c_m.m_id.id)
                str += "<option value='%s'>%s-%s</option>"%(c_m.m_id.id,c_m.m_id.m_id,c_m.m_id.name)
    return mark_safe(str)
    # for c_m in course_module:
