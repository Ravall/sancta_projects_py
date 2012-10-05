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
        verbose_name = 'Икона'


# события
class MfCalendarEvent(system_model.MfSystemObject):
    function = models.ForeignKey(MfCalendarSmartFunction)
    periodic = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'mf_calendar_event'
        managed = False
        app_label = 'sancta'

    def title(self):
        objectText = system_model.MfSystemObjectText.objects.get(system_object_id=self.id,status=u'Active').system_text
        return objectText.title