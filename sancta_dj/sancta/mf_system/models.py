# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

TEXT_STATUS_CHOICES = (
	(u'active', u'чистовик'),
    (u'draft', u'черновик'),
)

class MfSystemText(models.Model):
    title = models.CharField(max_length=250, blank=True)
    annonce = models.TextField(blank=True)
    content = models.TextField(blank=True)

    def __unicode__(self):
        return "%s" % self.title

    class Meta:
        db_table = u'mf_system_text'
        managed = False
        app_label = 'sancta'


class MfSystemObject(models.Model):
    status = models.CharField(max_length=21, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField()
    created_class = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='origin/')


    texts = models.ManyToManyField(MfSystemText, through='MfSystemObjectText')
    related_objects = models.ManyToManyField("self", through='MfSystemRelation')
    def __unicode__(self):
        return "%i" % self.id

    class Meta:
        db_table = u'mf_system_object'
        managed = False
        app_label = 'sancta'


class MfSystemObjectText(models.Model):
    system_object = models.ForeignKey(MfSystemObject)
    system_text = models.OneToOneField(MfSystemText)
    status = models.CharField(max_length=18,
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
    mf_object = models.ForeignKey(MfSystemObject)
    parent_object = models.ForeignKey(MfSystemObject)
    relation = models.ForeignKey(MfSystemRelationType)
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



