# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'Course.id'
        db.delete_column('planner_course', 'id')

        # Changing field 'Course.identifier'
        db.alter_column('planner_course', 'identifier', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True))

        # Adding unique constraint on 'Course', fields ['identifier']
        db.create_unique('planner_course', ['identifier'])
    
    
    def backwards(self, orm):
        
        # Adding field 'Course.id'
        db.add_column('planner_course', 'id', self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True), keep_default=False)

        # Changing field 'Course.identifier'
        db.alter_column('planner_course', 'identifier', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Removing unique constraint on 'Course', fields ['identifier']
        db.delete_unique('planner_course', ['identifier'])
    
    
    models = {
        'planner.breadthrequirement': {
            'Meta': {'object_name': 'BreadthRequirement'},
            'fulfillers': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Tag']"}),
            'min_courses': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'requirement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['planner.Requirement']", 'unique': 'True', 'primary_key': 'True'})
        },
        'planner.conjunctionrequirement': {
            'Meta': {'object_name': 'ConjunctionRequirement', '_ormbases': ['planner.Requirement']},
            'requirement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['planner.Requirement']", 'unique': 'True', 'primary_key': 'True'})
        },
        'planner.course': {
            'Meta': {'object_name': 'Course'},
            'class_number': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Instructor']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['planner.Tag']", 'through': "orm['planner.TagMapping']", 'symmetrical': 'False'}),
            'units': ('django.db.models.fields.IntegerField', [], {})
        },
        'planner.courseoffering': {
            'Meta': {'unique_together': "(('course', 'year', 'term', 'weekdays', 'start_time'),)", 'object_name': 'CourseOffering'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Course']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 50)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 0)'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Term']"}),
            'weekdays': ('django.db.models.fields.CharField', [], {'default': "'MWF'", 'max_length': '5'}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Year']"})
        },
        'planner.depthrequirement': {
            'Meta': {'object_name': 'DepthRequirement'},
            'fulfillers': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Tag']"}),
            'min_units': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'requirement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['planner.Requirement']", 'unique': 'True', 'primary_key': 'True'})
        },
        'planner.disjunctionrequirement': {
            'Meta': {'object_name': 'DisjunctionRequirement', '_ormbases': ['planner.Requirement']},
            'requirement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['planner.Requirement']", 'unique': 'True', 'primary_key': 'True'})
        },
        'planner.enrollment': {
            'Meta': {'unique_together': "(('plan', 'term', 'year', 'course'),)", 'object_name': 'Enrollment'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.CourseOffering']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Plan']"}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Term']"}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Year']"})
        },
        'planner.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'planner.major': {
            'Meta': {'object_name': 'Major'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'planner.plan': {
            'Meta': {'object_name': 'Plan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Major']"}),
            'num_years': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'start_year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Year']"}),
            'student_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'university': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['planner.University']", 'unique': 'True'})
        },
        'planner.requirement': {
            'Meta': {'object_name': 'Requirement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'planner.requirementmapping': {
            'Meta': {'object_name': 'RequirementMapping'},
            'coursereq': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course_requirement'", 'to': "orm['planner.Requirement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logreq': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logical_requirement'", 'to': "orm['planner.Requirement']"})
        },
        'planner.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'planner.tagmapping': {
            'Meta': {'object_name': 'TagMapping'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Tag']"})
        },
        'planner.term': {
            'Meta': {'object_name': 'Term'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {})
        },
        'planner.university': {
            'Meta': {'object_name': 'University'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_units_per_quarter': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'quarter_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'planner.year': {
            'Meta': {'object_name': 'Year'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_num': ('django.db.models.fields.IntegerField', [], {})
        }
    }
    
    complete_apps = ['planner']
