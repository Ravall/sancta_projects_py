# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.conf import settings


class Migration(SchemaMigration):

    def forwards(self, orm):
        if not settings.IS_TESTING:
            # только накатываем в режиме тестирования
            return
        tables = db.execute('show tables')
        if not ('mf_system_object',) in tables:
            db.execute("\
                CREATE TABLE `mf_system_object` (\
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT ' id',\
                    `parent_id` int(11) unsigned DEFAULT NULL COMMENT '  ,  ',\
                    `user_id` int(11) unsigned DEFAULT NULL COMMENT ',  ',\
                    `status` enum('active','pause','deleted') DEFAULT 'active' COMMENT '  ',\
                    `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT ' ',\
                    `updated` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',\
                    `created_class` varchar(100) DEFAULT NULL COMMENT '  ',\
                    `parent_ids` text COMMENT ',  id   ',\
                    `image` varchar(255) DEFAULT NULL,\
                    `url` varchar(250) DEFAULT NULL,\
                    `site_id` int(11) DEFAULT '1',\
                PRIMARY KEY (`id`),\
                UNIQUE KEY `url` (`url`),\
                KEY `FK_systemObjectParentId_systemObjectId` (`parent_id`),\
                KEY `FK_systemObjectUserId_systemUserId` (`user_id`)\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
            )
        if not ('mf_system_relation_type',) in tables:
            db.execute("\
                CREATE TABLE `mf_system_relation_type` (\
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                    `relation_name` varchar(255) DEFAULT '',\
                PRIMARY KEY (`id`)\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
            )
        if not ('mf_system_relation',) in tables:
            db.execute("\
                CREATE TABLE `mf_system_relation` (\
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                    `mf_object_id` int(11) unsigned NOT NULL,\
                    `parent_object_id` int(11) unsigned NOT NULL,\
                    `relation_id` int(11) unsigned NOT NULL,\
                PRIMARY KEY (`id`),\
                KEY `relation_to_relationtype` (`relation_id`),\
                KEY `related_by_parent` (`parent_object_id`,`relation_id`),\
                KEY `related_by_object` (`mf_object_id`,`relation_id`),\
                CONSTRAINT `parent_to_object` FOREIGN KEY (`parent_object_id`)\
                    REFERENCES `mf_system_object` (`id`),\
                CONSTRAINT `relation_to_relationtype`\
                    FOREIGN KEY (`relation_id`)\
                 REFERENCES `mf_system_relation_type` (`id`)\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
            )

        if not ('mf_system_text',) in tables:
            db.execute("\
                CREATE TABLE `mf_system_text` (\
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT \
                        COMMENT 'object_id',\
                    `title` varchar(250) DEFAULT NULL,\
                    `annonce` text,\
                    `content` text,\
                PRIMARY KEY (`id`)\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT=' .';"
            )
        if not ('mf_system_object_text',) in tables:
            db.execute("\
                CREATE TABLE `mf_system_object_text` (\
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT \
                        COMMENT '  (, )',\
                    `system_object_id` int(11) unsigned NOT NULL \
                        COMMENT '  ',\
                    `system_text_id` int(11) unsigned NOT NULL \
                        COMMENT '  ',\
                    `status` enum('active','draft') NOT NULL \
                        DEFAULT 'active',\
                PRIMARY KEY (`id`),\
                UNIQUE KEY `system_object_id` (`system_object_id`,`status`),\
                UNIQUE KEY `NewIndex_systemObjectId_lang` \
                    (`system_object_id`),\
                KEY `FK_systemObjectTextSystemTextId_SystemTextId`\
                    (`system_text_id`),\
                CONSTRAINT `FK_systemObjectTextSystemObjectId_SystemObjectId`\
                    FOREIGN KEY (`system_object_id`) \
                    REFERENCES `mf_system_object` (`id`) \
                    ON DELETE CASCADE ON UPDATE CASCADE,\
                CONSTRAINT `FK_systemObjectTextSystemTextId_SystemTextId`\
                    FOREIGN KEY (`system_text_id`)\
                    REFERENCES `mf_system_text` (`id`) \
                    ON DELETE CASCADE ON UPDATE CASCADE\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='   ';"
            )

        if not ('mf_system_article',) in tables:
            db.execute("\
                CREATE TABLE `mf_system_article` (\
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                    `mfsystemobject_ptr_id` int(11) unsigned DEFAULT NULL,\
                KEY `FK_mf_system_article` (`id`),\
                KEY `mfsystemobject_ptr_id` (`mfsystemobject_ptr_id`),\
                CONSTRAINT `mf_system_article_ibfk_1` \
                    FOREIGN KEY (`mfsystemobject_ptr_id`) \
                    REFERENCES `mf_system_object` (`id`)\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
            )

        if not ('mf_calendar_smart_function',) in tables:
            db.execute("\
                CREATE TABLE `mf_calendar_smart_function` (\
                    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,\
                    `smart_function` VARCHAR(255) DEFAULT NULL,\
                    `reload` TINYINT(1) DEFAULT '1',\
                PRIMARY KEY (`id`),\
                    KEY `NewIndex1` (`reload`)\
                ) ENGINE=INNODB DEFAULT CHARSET=utf8;"
            )

        if not ('mf_calendar_event',) in tables:
            db.execute("\
                CREATE TABLE `mf_calendar_event` (\
                    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,\
                    `mfsystemobject_ptr_id` int(11) unsigned NOT NULL,\
                    `smart_function` VARCHAR(255) DEFAULT NULL,\
                    `reload` TINYINT(1) DEFAULT '1',\
                    `function_id` INT(11) UNSIGNED NOT NULL,\
                    `periodic` TINYINT(1) DEFAULT '0',\
                PRIMARY KEY (`id`),\
                    KEY `event_to_function` (`function_id`),\
                CONSTRAINT `event_to_function`\
                    FOREIGN KEY (`function_id`) \
                    REFERENCES `mf_calendar_smart_function` (`id`),\
                CONSTRAINT `FK_event_to_object_new` \
                    FOREIGN KEY (`mfsystemobject_ptr_id`) \
                    REFERENCES `mf_system_object` (`id`)\
                ) ENGINE=INNODB DEFAULT CHARSET=utf8 COMMENT=' ';"
            )

        if not ('mf_calendar_icon',) in tables:
            db.execute("\
                CREATE TABLE `mf_calendar_icon` (\
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                    `mfsystemobject_ptr_id` int(11) unsigned NOT NULL,\
                PRIMARY KEY (`id`)\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
            )

        if not ('mf_calendar_net',) in tables:
            db.execute("\
                CREATE TABLE `mf_calendar_net` (\
                    `id` int(11) NOT NULL AUTO_INCREMENT,\
                    `full_date` date DEFAULT NULL,\
                    `function_id` int(11) unsigned DEFAULT NULL,\
                PRIMARY KEY (`id`),\
                UNIQUE KEY `NewIndexFullDate_EventId` (`full_date`,`function_id`),\
                KEY `FK_mfCalendarNetEventId_mfCalendarEventId` (`function_id`),\
                KEY `full_date_index` (`full_date`) \
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8 \
                 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;"
            )

    def backwards(self, orm):
        pass

    complete_apps = ['sancta']
