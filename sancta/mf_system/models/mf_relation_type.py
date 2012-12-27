# -*- coding: utf-8 -*-
from django.db import models


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
        verbose_name_plural = 'Типы связей объектов с объектами'
