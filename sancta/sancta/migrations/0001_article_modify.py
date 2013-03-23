# -*- coding: utf-8 -*-
from south.db import dbs
from south.v2 import SchemaMigration
from django.conf import settings


class Migration(SchemaMigration):

    def forwards(self, orm):
        if settings.IS_TESTING:
            return
        dbs['sancta_db'].start_transaction()
        try:
            dbs['sancta_db'].delete_foreign_key('mf_system_article', 'id')
            dbs['sancta_db'].execute(
                'ALTER TABLE `mf_system_article` CHANGE `id` '\
                '`id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT, ADD PRIMARY KEY(`id`);'
            )
            dbs['sancta_db'].execute(
                'ALTER TABLE `mf_system_article` '\
                'ADD COLUMN `mfsystemobject_ptr_id` '\
                'INT(11) UNSIGNED AFTER `id`'
            )
            dbs['sancta_db'].execute(
                'ALTER TABLE `mf_system_article` ADD CONSTRAINT '\
                '`FK_article` FOREIGN KEY (`mfsystemobject_ptr_id`) '\
                'REFERENCES `mf_system_object` (`id`);'
            )
            dbs['sancta_db'].execute(
                'UPDATE `mf_system_article` SET `mfsystemobject_ptr_id`=`id`'
            )
            dbs['sancta_db'].commit_transaction()
        except:
            dbs['sancta_db'].rollback_transaction()

    def backwards(self, orm):
        # откатывать? а зачем?)
        pass

    complete_apps = ['sancta']
