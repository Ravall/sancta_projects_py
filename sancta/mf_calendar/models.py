# -*- coding: utf-8 -*-
from django.db import models
from mf_system import models as system_model

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

    class Meta:
        db_table = u'mf_calendar_event'
        managed = False
        app_label = 'sancta'
        verbose_name = 'событие календаря'
        verbose_name_plural = 'События календаря'