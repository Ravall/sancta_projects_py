# -*- coding: utf-8 -*-
from south.db import dbs
from south.v2 import SchemaMigration
from django.conf import settings


class Migration(SchemaMigration):
    def forwards(self, orm):
        #if settings.IS_TESTING:
        #    return
        dbs['sancta_db'].start_transaction()
        try:
            if not ('django_content_type',)\
                in dbs['sancta_db'].execute('show tables'):
                dbs['sancta_db'].execute(
                    "CREATE VIEW django_content_type AS "\
                    "SELECT * FROM {0}.django_content_type"\
                    .format(settings.DATABASES['default']['NAME'])
                )
            dbs['sancta_db'].commit_transaction()
        except Exception, e:
            dbs['sancta_db'].rollback_transaction()
            raise e

    def backwards(self, orm):
        pass

    complete_apps = ['sancta']
