# -*- coding: utf-8 -*-

from django.db import models

TEXT_STATUS_CHOICES = (
	(u'Active', u'Active'),
    (u'Draft', u'Draft'),
)

class MfSystemText(models.Model):
    title = models.CharField(max_length=250, blank=True)
    annonce = models.TextField(blank=True)
    content = models.TextField(blank=True)
    class Meta:
        db_table = u'mf_system_text'
        managed = False
        app_label = 'sancta'


class MfSystemObject(models.Model):
    parent_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=21, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField()
    created_class = models.CharField(max_length=250, blank=True)
    parent_ids = models.TextField(blank=True)
    image = models.CharField(max_length=250, blank=True)
    class Meta:
        db_table = u'mf_system_object'
        managed = False
        app_label = 'sancta'


class MfSystemObjectText(models.Model):
    system_object = models.ForeignKey(MfSystemObject, unique=True)
    system_text = models.ForeignKey(MfSystemText)
    status = models.CharField(max_length=18,
    						  unique=True,
    						  choices=TEXT_STATUS_CHOICES)
    class Meta:
        db_table = u'mf_system_object_text'
        managed = False
        app_label = 'sancta'


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
    class Meta:
        db_table = u'mf_calendar_event'
        managed = False
        app_label = 'sancta'

    def title(self):
        objectText = MfSystemObjectText.objects.get(system_object_id=self.id,status=u'Active').system_text
        return objectText.title


# статьи
class MfSystemArticle(models.Model):
    class Meta:
        db_table = u'mf_system_article'
        managed = False
        app_label = 'sancta'

    def title(self):
        objectText = MfSystemObjectText.objects.get(system_object_id=self.id,status=u'Active').system_text

        return objectText.title

