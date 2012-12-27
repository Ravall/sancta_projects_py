# -*- coding: utf-8 -*-
from django.conf import settings
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    no_dry_run = True

    def forwards(self, orm):
        if settings.IS_TESTING:
            return
        orm['sancta.mfsystemarticle'].objects.update(
            created_class='MfSystemArticle'
        )

    def backwards(self, orm):
        pass

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sancta.mfcalendarevent': {
            'Meta': {'managed': 'False', 'object_name': 'MfCalendarEvent', 'db_table': "u'mf_calendar_event'", '_ormbases': ['sancta.MfSystemObject']},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sancta.MfCalendarSmartFunction']"}),
            'mfsystemobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sancta.MfSystemObject']", 'unique': 'True', 'primary_key': 'True'}),
            'periodic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'sancta.mfcalendaricon': {
            'Meta': {'managed': 'False', 'object_name': 'MfCalendarIcon', 'db_table': "u'mf_calendar_icon'", '_ormbases': ['sancta.MfSystemObject']},
            'mfsystemobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sancta.MfSystemObject']", 'unique': 'True', 'primary_key': 'True'})
        },
        'sancta.mfcalendarnet': {
            'Meta': {'object_name': 'MfCalendarNet', 'db_table': "u'mf_calendar_net'", 'managed': 'False'},
            'full_date': ('django.db.models.fields.DateField', [], {}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sancta.MfCalendarSmartFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sancta.mfcalendarsmartfunction': {
            'Meta': {'object_name': 'MfCalendarSmartFunction', 'db_table': "u'mf_calendar_smart_function'", 'managed': 'False'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reload': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'smart_function': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'})
        },
        'sancta.mfsystemarticle': {
            'Meta': {'managed': 'False', 'object_name': 'MfSystemArticle', 'db_table': "u'mf_system_article'", '_ormbases': ['sancta.MfSystemObject']},
            'mfsystemobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sancta.MfSystemObject']", 'unique': 'True', 'primary_key': 'True'})
        },
        'sancta.mfsystemobject': {
            'Meta': {'object_name': 'MfSystemObject', 'db_table': "u'mf_system_object'", 'managed': 'False'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_class': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'related_objects': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related'", 'symmetrical': 'False', 'through': "orm['sancta.MfSystemRelation']", 'to': "orm['sancta.MfSystemObject']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '21'}),
            'texts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sancta.MfSystemText']", 'through': "orm['sancta.MfSystemObjectText']", 'symmetrical': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'sancta.mfsystemobjecttext': {
            'Meta': {'object_name': 'MfSystemObjectText', 'db_table': "u'mf_system_object_text'", 'managed': 'False'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'system_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sancta.MfSystemObject']"}),
            'system_text': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sancta.MfSystemText']", 'unique': 'True'})
        },
        'sancta.mfsystemrelation': {
            'Meta': {'object_name': 'MfSystemRelation', 'db_table': "u'mf_system_relation'", 'managed': 'False'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mf_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_object'", 'to': "orm['sancta.MfSystemObject']"}),
            'parent_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_parent_object'", 'to': "orm['sancta.MfSystemObject']"}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sancta.MfSystemRelationType']"})
        },
        'sancta.mfsystemrelationtype': {
            'Meta': {'object_name': 'MfSystemRelationType', 'db_table': "u'mf_system_relation_type'", 'managed': 'False'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relation_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'sancta.mfsystemtext': {
            'Meta': {'object_name': 'MfSystemText', 'db_table': "u'mf_system_text'", 'managed': 'False'},
            'annonce': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['sancta']