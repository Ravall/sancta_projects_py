# -*- coding: utf-8 -*-
from django.db import models
from mf_system import models as system_model
from tools import extra

# функции
class MfCalendarSmartFunction(models.Model):
    smart_function = models.CharField(max_length=765, blank=True)
    reload = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.smart_function

    class Meta:
        db_table = u'mf_calendar_smart_function'
        managed = False
        app_label = 'sancta'

class MfCalendarIcon(system_model.MfSystemObject):
    objects = system_model.SystemObjectManager()

    @classmethod
    def get_by_events(cls, events):
        return system_model.MfSystemRelation.objects.filter(
            relation_id=2,
            parent_object_id__in=[event['id'] for event in events],
            mf_object__status='active'
        ).extra(
            **(system_model.SystemObjectManager.get_extra_for_text(
                'mf_system_object.id'
            ))
        ).extra(**extra.icon_table()).order_by('?')


    class Meta:
        db_table = u'mf_calendar_icon'
        managed = False
        app_label = 'sancta'
        verbose_name = 'икона'
        verbose_name_plural = 'Иконы'


# события
class MfCalendarEvent(system_model.MfSystemObject):
    function = models.ForeignKey(MfCalendarSmartFunction)
    periodic = models.IntegerField(null=True, blank=True)

    objects = system_model.SystemObjectManager()
    def get_icons(self):
        return self.related_objects.filter(
            created_class='MfCalendarIcon',
            status='active'
        ).extra(
            **(system_model.SystemObjectManager.get_extra_for_text(
                'mf_system_object.id'
            ))
        ).extra(**extra.icon_table())


    class Meta:
        db_table = u'mf_calendar_event'
        managed = False
        app_label = 'sancta'
        verbose_name = 'событие календаря'
        verbose_name_plural = 'События календаря'

class CalendarManager(models.Manager):
    def get_query_set(self):
        return super(CalendarManager, self).get_query_set().extra(
            select={
                'event_id':'mf_calendar_event.id',
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