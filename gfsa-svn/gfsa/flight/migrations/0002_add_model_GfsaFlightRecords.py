# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'GfsaFlightRecords'
        db.create_table('gfsa_flight_records', (
            ('fr_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tug_tug',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tug.GfsaTugs'], db_column='Tug_tug_id')),
            ('glider_glider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['glider.GfsaGliders'],
                                                                                    db_column='Glider_glider_id')),
            ('fr_p1_id', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('fr_p2_id', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('fr_p1_pay_percent', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('fr_p2_pay_percent', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('fr_take_off', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('fr_tug_land', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('fr_glider_land', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('fr_tug_duration', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('fr_glider_duration', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('fr_special', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('fr_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fr_last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'flight', ['GfsaFlightRecords'])


    def backwards(self, orm):
        # Deleting model 'GfsaFlightRecords'
        db.delete_table('gfsa_flight_records')


    models = {
        u'flight.gfsaflightrecords': {
            'Meta': {'object_name': 'GfsaFlightRecords', 'db_table': "'gfsa_flight_records'", 'managed': 'False'},
            'fr_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fr_glider_duration': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'fr_glider_land': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'fr_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'fr_last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'fr_p1_id': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'fr_p1_pay_percent': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'fr_p2_id': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'fr_p2_pay_percent': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'fr_special': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'fr_take_off': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'fr_tug_duration': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'fr_tug_land': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'glider_glider': ('django.db.models.fields.related.ForeignKey', [],
                              {'to': u"orm['glider.GfsaGliders']", 'db_column': "'Glider_glider_id'"}),
            'tug_tug': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': u"orm['tug.GfsaTugs']", 'db_column': "'Tug_tug_id'"})
        },
        u'glider.gfsagliders': {
            'Meta': {'object_name': 'GfsaGliders', 'db_table': "'gfsa_gliders'", 'managed': 'False'},
            'glider_accepted_launch_type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'glider_active': ('django.db.models.fields.BooleanField', [], {}),
            'glider_flarm_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'glider_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'glider_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '45'}),
            'glider_other_text_description': (
                'django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'glider_owner': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'glider_seat_type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'glider_total_flights': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'glider_total_flying_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
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

    complete_apps = ['flight']