# -*- coding: utf-8 -*-
from django.db import models
from mf_system.models.mf_object import MfSystemObject
from mf_system.models.object_manager import SystemObjectManager
from mf_system.models import MfSystemRelation, MfSystemArticle
from smart_date import smartfunction


# функции
class MfCalendarSmartFunction(models.Model):
    smart_function = models.CharField(max_length=765, blank=True)
    reload = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.smart_function

    def getDates(self, year):
        return smartfunction.generate(self.smart_function, year)

    class Meta:
        db_table = u'mf_calendar_smart_function'
        managed = False
        app_label = 'sancta'


class MfCalendarIcon(MfSystemObject):
    objects = SystemObjectManager('mfsystemobject_ptr_id')

    def __init__(self, *args, **kwargs):
        kwargs['created_class'] = 'MfCalendarIcon'
        super(MfCalendarIcon, self).__init__(*args, **kwargs)

    class Meta:
        db_table = u'mf_calendar_icon'
        managed = False
        app_label = 'sancta'
        verbose_name = 'icon'
        verbose_name_plural = 'Иконы'


class EventObjectManager(SystemObjectManager):
    '''
    расширим objects у MfCalendarEvent
    присоединим к модели событие - данные о фунции.
    '''

    @staticmethod
    def get_extra_for_event():
        return {
            'select': {
                'smart_function': 'mf_calendar_smart_function.smart_function',
                'count_icons': 'SELECT count(*) FROM mf_system_relation srlt\
                     WHERE `srlt`.`parent_object_id` = \
                        `mf_calendar_event`.`mfsystemobject_ptr_id` \
                     AND relation_id = 2',
                'count_articles': 'SELECT count(*) FROM mf_system_relation srlt\
                     WHERE `srlt`.`parent_object_id` = \
                        `mf_calendar_event`.`mfsystemobject_ptr_id` \
                     AND relation_id = 1',
            },
            'tables': [
                'mf_calendar_smart_function'
            ],
            'where': [
                'mf_calendar_smart_function.id = mf_calendar_event.function_id'
            ]
        }

    def get_query_set(self):
        return super(EventObjectManager, self).get_query_set().extra(
            **EventObjectManager.get_extra_for_event()
        )


class MfCalendarEvent(MfSystemObject):

    function = models.ForeignKey(MfCalendarSmartFunction)
    periodic = models.IntegerField(null=True, blank=True)
    objects = EventObjectManager('mf_calendar_event.mfsystemobject_ptr_id')


    def add_icon(self, icon):
        # привязываем икону к редактируемому объекту
        relation = MfSystemRelation(
            relation_id=2,
            parent_object=self,
            mf_object=icon
        )
        relation.save()

    def get_icons(self):
        icons_ids = [
            icon.id for icon in
            self.related_objects.filter(
                status='active',
                created_class='MfCalendarIcon'
            )
        ]
        return MfCalendarIcon.objects.filter(id__in=icons_ids)

    def get_articles(self):
        articles_ids = [
            article.id for article in
            self.related_objects.filter(
                status='active',
                created_class='MfSystemArticle'
            )
        ]
        return MfSystemArticle.objects.filter(id__in=articles_ids)

    class Meta:
        db_table = u'mf_calendar_event'
        managed = False
        app_label = 'sancta'
        verbose_name = u'calendar event'
        verbose_name_plural = 'События календаря'


class CalendarManager(models.Manager):
    def get_query_set(self):
        return super(CalendarManager, self).get_query_set().extra(
            select={
                'event_id': 'mf_system_object.id',
            },
            tables=[
                'mf_calendar_event',
                'mf_system_object'
            ],
            where=[
                'mf_calendar_event.function_id=mf_calendar_net.function_id',
                'mf_system_object.id=mf_calendar_event.mfsystemobject_ptr_id',
                'mf_system_object.status = %s'
            ],
            params=[
                'Active',
            ]
        )


# сетка календаря
# TODO удалить поля day,month,year,event_id и связанные с ними индексы
class MfCalendarNet(models.Model):
    full_date = models.DateField()
    function = models.ForeignKey(MfCalendarSmartFunction)

    objects = CalendarManager()

    class Meta:
        db_table = u'mf_calendar_net'
        managed = False
        app_label = 'sancta'
