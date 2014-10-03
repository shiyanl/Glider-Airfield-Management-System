# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        pass

    def backwards(self, orm):
        pass

    models = {
        u'tug.gfsatugs': {
            'Meta': {'object_name': 'GfsaTugs', 'db_table': "'gfsa_tugs'", 'managed': 'False'},
            'tug_active': ('django.db.models.fields.BooleanField', [], {}),
            'tug_flarm_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tug_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tug_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '45'}),
            'tug_owner': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'tug_text_description': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['tug']