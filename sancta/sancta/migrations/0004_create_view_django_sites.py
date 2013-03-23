# -*- coding: utf-8 -*-
from south.db import dbs
from south.v2 import SchemaMigration
from django.conf import settings
from tools.db_helper import is_table_exists


class Migration(SchemaMigration):
    def forwards(self, orm):
        if settings.IS_TESTING:
            return
        if not is_table_exists(dbs['sancta_db'], 'django_site'):
            dbs['sancta_db'].execute(
                "CREATE VIEW django_site AS "
                "SELECT * FROM {0}.django_site"
                .format(settings.DATABASES['default']['NAME'])
            )

    def backwards(self, orm):
        pass

    complete_apps = ['sancta']
