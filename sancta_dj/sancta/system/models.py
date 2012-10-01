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

    def __unicode__(self):
        return "%i" % self.id

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

# статьи
class MfSystemArticle(models.Model):
    class Meta:
        db_table = u'mf_system_article'
        managed = False
        app_label = 'sancta'

    def title(self):
        objectText = MfSystemObjectText.objects.get(system_object_id=self.id,status=u'Active').system_text

        return objectText.title

# типы связей
class MfSystemRelationType(models.Model):
    relation_name = models.CharField(max_length=250, blank=True)

    def __unicode__(self):
        return self.relation_name

    class Meta:
        db_table = u'mf_system_relation_type'
        managed = False
        app_label = 'sancta'
        verbose_name = 'тип связи'
        verbose_name_plural = 'Типы связей объектов с объектамиs'

# сами связи
class MfSystemRelation(models.Model):
    object = models.ForeignKey(MfSystemObject)
    parent = models.ForeignKey(MfSystemObject)
    type = models.ForeignKey(MfSystemRelationType)
    class Meta:
        db_table = u'mf_system_relation'
        managed = False
        app_label = 'sancta'

# файлы
class MfSystemFile(models.Model):
    object = models.ForeignKey(MfSystemObject)
    class Meta:
        db_table = u'mf_system_file'
        managed = False
        app_label = 'sancta'



