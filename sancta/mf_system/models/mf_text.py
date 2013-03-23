# -*- coding: utf-8 -*-
from django.db import models


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
