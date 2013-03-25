# -*- coding: utf-8 -*-
# pylint: disable=E1102

'''
САБНАК - демон, ответственный за гниение трупов.
------------
удаляет старый кэш
    update_event вызывается при сохранении события
    подчистить по урлу:
        event/[id]
        event/[url новый]
        event/[url старый]
        calendar/(все даты по новому smart_function)
        calendar/(все даты по старому smart_function)
        article[id добавленной статьи]
        article[url добавленной статьи]
            теги статей не трогаем т.к нельзя добавить тегированную статью
        article[id всех привязанных статей к событию]
        article[url всех привязанных статей к событию]
    update_article вызывается при сохранении статьи
    подчистить по урлам:
        article[id]
        article[url новый]
        article[url старый]
        article[tags старые]
        article[tags новые]
        event/[id к которому привязана статья]
        event/[url к которому привязана статья]
        calendar/(все даты по smart_function события,
            к которому привязана статья)

'''
import celery
import logging
from api import cc
from mf_system.models import MfSystemArticle
from mf_calendar.models import MfCalendarEvent, MfCalendarIcon


@celery.task()
def update_event(obj, cleaned_data):
    assert isinstance(obj, MfCalendarEvent)
    """
    методы по очистки кэша при обновлении события
    event_id - идентификатор события
    cleaned_data - форма данных
    """
    logger = logging.getLogger('sancta_log')
    logger.info('сохранение события')

    #очистим кеш и информацию о событии
    if obj.id:
        cc.by_event_id(obj.id)
        cc.by_event_url(obj.url)
        if obj.function != cleaned_data['smart_function']:
            cc.by_smart_function(obj.function.smart_function)
    cc.by_event_url(cleaned_data['seo_url'])
    cc.by_smart_function(cleaned_data['smart_function'])

    if cleaned_data['add_article']:
        #если была добавлена статья
        article = MfSystemArticle.objects.get(
            pk=cleaned_data['add_article']
        )
        cc.by_article_url(article.url)
        cc.by_article_id(article.id)
    #чистим привязанные статьи
    if obj.id:
        for obj_art in obj.get_articles():
            cc.by_article_url(obj_art.url)
            cc.by_article_id(obj_art.id)
    logger.info('save_model end')


@celery.task()
def update_article(obj, cleaned_data):
    assert isinstance(obj, MfSystemArticle)
    if obj.id:
        # основные параметры
        cc.by_article_url(obj.url)
        cc.by_article_id(obj.id)
        # пройдемся по существующим тегам
        for tag in obj.tags.all():
            cc.by_article_tag(tag.name)
        # пройдемся по привязанным статьям
        parent_relateds = obj.get_relate_to()
        for rel_obj in parent_relateds:
            if rel_obj.created_class == 'MfCalendarEvent':
                event = rel_obj
                cc.by_smart_function(event.smart_function)
                cc.by_event_id(event.id)
                cc.by_event_url(event.url)
    # пройдемся по новым тегам
    for tag in [
        art_tag.strip() for art_tag
        in cleaned_data['tags'].split(',')
        if art_tag.strip()
    ]:
        cc.by_article_tag(tag)
    # новый seo_url
    cc.by_article_url(cleaned_data['seo_url'])


@celery.task()
def update_icon(obj, cleaned_data):
    # pylint: disable=W0613
    assert isinstance(obj, MfCalendarIcon)
    if obj.id:
        parent_relateds = obj.get_relate_to()
        for rel_obj in parent_relateds:
            if rel_obj.created_class == 'MfCalendarEvent':
                event = rel_obj
                cc.by_event_id(event.id)
                cc.by_event_url(event.url)
                cc.by_smart_function(event.function.smart_function)