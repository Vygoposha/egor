from django import template

register = template.Library()


@register.filter(name='group_list')
def group_list(user):
    return list(user.groups.all().values_list('name', flat = True))