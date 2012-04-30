# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Course.weekdays'
        db.add_column('planner_course', 'weekdays', self.gf('django.db.models.fields.CharField')(default='MWF', max_length=6), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Course.weekdays'
        db.delete_column('planner_course', 'weekdays')
    
    
    models = {
        'planner.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'endTime': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 50)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'startTime': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 0)'}),
            'units': ('django.db.models.fields.IntegerField', [], {}),
            'weekdays': ('django.db.models.fields.CharField', [], {'default': "'MWF'", 'max_length': '6'})
        }
    }
    
    complete_apps = ['planner']
