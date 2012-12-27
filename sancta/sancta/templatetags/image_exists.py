# -*- coding: utf-8 -*-
import os
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def image_exists(file_name, crop_folder):
    return file_name if os.path.exists(
        settings.MEDIA_ROOT + '/' + crop_folder + '/' + str(file_name)
    ) else 'не загрузилось еще изображение'


@register.simple_tag
def image_tag(file_name, crop_folder):
    if file_name and os.path.exists(
        settings.MEDIA_ROOT + '/' + crop_folder + '/' + str(file_name)
    ):
        return '<img src="{2}{0}/{1}">'.format(crop_folder, file_name, settings.MEDIA_URL)
    else:
        return '<span>image {0} not loaded</span>'.format(file_name)
