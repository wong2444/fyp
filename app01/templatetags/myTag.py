from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def list_distinct(course_module, name):
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
                str += "<option value='%s'>%s-%s</option>" % (c_m.m_id.id, c_m.m_id.m_id, c_m.m_id.name)
    return mark_safe(str)
    # for c_m in course_module:


@register.simple_tag
def userList(user_list, attendance_record):
    str = ""
    for user in user_list:
        has_record = False
        for a_r in attendance_record:
            if user.id == a_r.s_id_id and a_r.is_abs is False:
                has_record = True
                str += "<tr>"
                str += "<th scope=\"row\"><input type=\"checkbox\" checked disabled></th>"
                str += "<td>" + user.s_id + "</td>"
                str += "<td>" + user.name + "</td>"
                if a_r.is_late:
                    str += "<td>" + a_r.arrive_time.strftime('%H:%M:%S') + " (late)</td>"
                else:
                    str += "<td>" + a_r.arrive_time.strftime('%H:%M:%S') + "</td>"

        if not has_record:
            str += "<tr>"
            str += "<th scope=\"row\"><input type=\"checkbox\" disabled></th>"
            str += "<td>" + user.s_id + "</td>"
            str += "<td>" + user.name + "</td>"
            str += "<td>-</td>"
    return mark_safe(str)
