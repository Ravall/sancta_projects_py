# -*- coding: utf-8 -*-
from django.db import models
from .mf_relation_type import MfSystemRelationType


# сами связи
class MfSystemRelation(models.Model):
    parent_object = models.ForeignKey(
        "MfSystemObject",
        related_name="to_parent_object"
    )
    mf_object = models.ForeignKey(
        "MfSystemObject",
        related_name="to_object"
    )
    relation = models.ForeignKey(MfSystemRelationType)

    def __unicode__(self):
        return self.relation.relation_name

    class Meta:
        db_table = u'mf_system_relation'
        managed = False
        app_label = 'sancta'
