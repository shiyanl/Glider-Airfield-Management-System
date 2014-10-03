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
        u'glider.gfsagliders': {
            'Meta': {'object_name': 'GfsaGliders', 'db_table': "'gfsa_gliders'", 'managed': 'False'},
            'glider_accepted_launch_type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'glider_active': ('django.db.models.fields.BooleanField', [], {}),
            'glider_flarm_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'glider_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'glider_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '45'}),
            'glider_other_text_description': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'glider_owner': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'glider_seat_type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'glider_total_flights': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'glider_total_flying_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['glider']