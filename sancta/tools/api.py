# -*- coding: utf-8 -*-
from django.conf import settings


def prepare_text(obj):
    '''
    вывод текст
    '''
    return dict(
        title=obj.title,
        annonce=obj.annonce,
        content=obj.content,
    )


def prepare_icon(icon):
    '''
    подготавливает для вывода в словарь икону
    '''
    return {
        'id': icon.id,
        'event_id': icon.event_id,
        'text': prepare_text(icon),
        'image': icon.image,
        'url': '{host}crop/*size*/{image_name}'.format(
            host=settings.MEDIA_HOST,
            image_name=icon.image
        ),
        'sizes': ['150x200', '600x800'],
    }


def prepare_icons(icons):
    return [prepare_icon(icon) for icon in icons]


def prepare_event(event):
    '''
    подготавливает для вывода в словарь событие
    '''
    return {
        'id': event.id,
        'text': prepare_text(event),
        'image': event.image,
        'icons': prepare_icons(event.get_icons()),
    }
