# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Course'
        db.create_table('planner_course', (
            ('endTime', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 50))),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('startTime', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 0))),
            ('units', self.gf('django.db.models.fields.IntegerField')()),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('planner', ['Course'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Course'
        db.delete_table('planner_course')
    
    
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
