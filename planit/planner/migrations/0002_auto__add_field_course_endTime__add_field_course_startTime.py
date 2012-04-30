# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Course.endTime'
        db.add_column('planner_course', 'endTime', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 50)), keep_default=False)

        # Adding field 'Course.startTime'
        db.add_column('planner_course', 'startTime', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 0)), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Course.endTime'
        db.delete_column('planner_course', 'endTime')

        # Deleting field 'Course.startTime'
        db.delete_column('planner_course', 'startTime')
    
    
    models = {
        'planner.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'endTime': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 50)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'startTime': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 0)'}),
            'units': ('django.db.models.fields.IntegerField', [], {})
        }
    }
    
    complete_apps = ['planner']
