# -*- coding: utf-8 -*-
def prepare_icon(icon):
    '''
    подготавливает для вывода в словарь икону
    '''
    return {
        'id': icon.id,
        'event_id': icon.event_id,
        'text': {
            'title': icon.title,
            'annonce': icon.annonce,
            'content': icon.content,
        },
        'image': icon.image,
        'urls': {
            'origin': 'http://img.sancta.ru/origin/%s' % icon.image,
           # '150x200': 'http://img.sancta.ru/crop/150x200/%s' % icon.image
            '150x200': 'http://127.0.0.1:8000/media/crop/150x200/%s' % icon.image,


        }
    }


def prepare_icons(icons):
    return [prepare_icon(icon) for icon in icons]