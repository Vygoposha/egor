from django import template

register = template.Library()


@register.filter(name='subscribers_list')
def subscribers_list(category):
    return list(category.subscribers.all().values_list('username', flat=True))
