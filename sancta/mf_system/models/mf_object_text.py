# -*- coding: utf-8 -*-
from django.db import models
from .mf_text import MfSystemText


TEXT_STATUS_CHOICES = (
    (u'active', u'чистовик'),
    (u'draft', u'черновик'),
)


class MfSystemObjectText(models.Model):
    system_object = models.ForeignKey('MfSystemObject')
    system_text = models.OneToOneField(MfSystemText)
    status = models.CharField(max_length=18,
                              choices=TEXT_STATUS_CHOICES)

    class Meta:
        db_table = u'mf_system_object_text'
        managed = False
        app_label = 'sancta'
