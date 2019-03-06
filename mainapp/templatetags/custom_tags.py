from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_folder_files')
def media_folder_files(string):
    if not string:
        string = 'default.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='currency')
def currency(string):
    return f'${string}'


@register.filter(name='is_active_list')
def is_active_list(object_list):
    object_list = object_list.filter(is_active='True')
    return object_list
