# -*- coding: utf-8 -*-
from south.db import dbs
from south.v2 import SchemaMigration
from django.db import models
from tools.db_helper import is_column_exists
from django.conf import settings


class Migration(SchemaMigration):

    def forwards(self, orm):
        if settings.IS_TESTING:
            # только накатываем не в режиме тестирования
            return
        if not is_column_exists(dbs['sancta_db'],'mf_system_object', 'site_id'):
            dbs['sancta_db'].add_column(
                'mf_system_object',
                'site_id',
                models.IntegerField(null=True, default=1)
             )
            dbs['sancta_db'].create_index('mf_system_object', ['site_id'])

    def backwards(self, orm):
        pass

    complete_apps = ['sancta']
