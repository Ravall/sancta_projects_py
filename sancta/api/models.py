# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import requests


def typograf(text):
    if not len(text):
        return ''
    try:
        url = "http://www.typograf.ru/webservice/"
        request = requests.post(url, {"text":text, "chr": 'UTF-8'})
        request.raise_for_status()
        result = request.content
    except Exception:
        result = text
    return result


def prepare_text(obj):
    """
    вывод текста
    """
    return dict(
        title=obj.title,
        annonce=typograf(obj.annonce),
        content=typograf(obj.content),
    )


def prepare_icon(icon, **kwargs):
    """
    выводит информацию о иконе
    """
    data = prepare_object(icon, **kwargs)
    data['image'] = str(icon.image)
    return data


def prepare_icons(icons, **kwargs):
    """
    выводит список икон
    """
    return [
        prepare_icon(icon, **kwargs)
        for icon in icons
        # если есть картинка (нет картинки - нет иконы)
        if icon and icon.image != ''
    ]


def prepare_article(article, **kwargs):
    """
    выводит информацию об одной статье
    """
    data = prepare_object(article, **kwargs)
    return data


def prepare_articles(articles):
    """
    выводит список статей
    """
    return [
        prepare_article(
            article, add_related=False, show_text=False
        )
        for article in articles
    ]


def prepare_event(event, **kwargs):
    """
    выводит инорфмацию об одном событии
    """
    data = prepare_object(event, **kwargs)
    # выведем умную фунцию
    data['smart_date'] = event.function.smart_function
    if kwargs.get('show_icons', True):
        icons = event.get_icons()
        if icons:
            data['icons'] = prepare_icons(icons)
    if kwargs.get('show_articles', True):
        articles = event.get_articles()
        if articles:
            data['articles'] = prepare_articles(articles)
    return data


def prepare_events(events):
    """
    выводит список статей
    """
    return [
        prepare_event(
            event, add_related=False, show_text=False,
            show_articles=False, show_icons=False
        )
        for event in events
    ]


def get_type(created_class):
    """
    передает на вывод тип объекта -
    переводит внутренний created_class в значение,
    для отображения пользователю
    """
    types = {
        'MfSystemArticle': 'article',
        'MfCalendarEvent': 'event',
        'MfCalendarIcon': 'icon',
    }
    return types.get(created_class, '')


def prepare_object(text_object, **kwargs):
    """
    выводит информацию об объекте - все то общее,
    что есть у всех моделей
    """
    data = {
        'id': text_object.id,
        'image': str(text_object.image),
        'type': get_type(text_object.created_class)
    }
    tags = text_object.tags.all()
    if tags:
        # если у объекта есть теги - то выводим их названия
        data['tags'] = [tag.name for tag in tags]
    # если показывать текст полностью - выводим секцию
    # text = {'title':???, 'annonce': ???, 'content': ???}
    # в проитвном случае - выдаем текст в общей секции
    if kwargs.get('show_text', True):
        data['text'] = prepare_text(text_object)
    else:
        data['title'] = text_object.title

    if text_object.url:
        data['name'] = text_object.url

    if kwargs.get('add_related', False) and text_object.is_related():
        data['related'] = []
        for rel_obj in text_object.get_relate_to():
            api_type = get_type(rel_obj.created_class)
            if api_type:
                # если тип объекта к которому "я" привязан  и если
                # удалось определить то возвращем его
                data['related'].append(
                    prepare_object(rel_obj, show_text=False)
                )
    return data


class NotificationEmail(models.Model):
    email = models.EmailField()

    class Meta:
        db_table = u'api_nofify_email'
        managed = False
        app_label = 'api'
