# -*- coding: utf-8 -*-
from django.db import models
from system import models as sys

# функции
class MfCalendarSmartFunction(models.Model):
    smart_function = models.CharField(max_length=765, blank=True)
    reload = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'mf_calendar_smart_function'
        managed = False
        app_label = 'sancta'


# события
class MfCalendarEvent(models.Model):
    smart_function = models.CharField(max_length=765, blank=True)
    reload = models.IntegerField(null=True, blank=True)
    function = models.ForeignKey(MfCalendarSmartFunction)
    periodic = models.IntegerField(null=True, blank=True)

    icons = models.ManyToManyField(sys.MfSystemFile)
    class Meta:
        db_table = u'mf_calendar_event'
        managed = False
        app_label = 'sancta'

    def title(self):
        objectText = sys.MfSystemObjectText.objects.get(system_object_id=self.id,status=u'Active').system_text
        return objectText.title