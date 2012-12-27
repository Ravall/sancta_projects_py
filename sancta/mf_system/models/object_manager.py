# -*- coding: utf-8 -*-
from django.db import models


class SystemObjectManager(models.Manager):

    def __init__(self, field=None):
        super(SystemObjectManager, self).__init__()
        self.field = field

    def get_extra_for_text(self):
        return {
            'select': {
                'title': 'mf_system_text.title',
                'annonce': 'mf_system_text.annonce',
                'content': 'mf_system_text.content',
            },
            'tables': [
                'mf_system_text',
                'mf_system_object_text'
            ],
            'where': [
                'mf_system_object_text.system_object_id = {0}'.format(self.field),
                'mf_system_object_text.status = %s',
                'mf_system_object_text.system_text_id = mf_system_text.id',
            ],
            'params': [
                'Active',
            ]
        }

    def get_query_set(self):
        """
        что бы при запросе к объектным моделям были еще добавлены
        активные (не черновик) тексты (title, annonce, content) изменяем запрос
        """
        return super(SystemObjectManager, self).get_query_set().extra(
            **self.get_extra_for_text()
        )
