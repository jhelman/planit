# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting model 'Year'
        db.delete_table('planner_year')

        # Adding model 'Prereq'
        db.create_table('planner_prereq', (
            ('prereq', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prereq', to=orm['planner.Course'])),
            ('mandatory', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='for', to=orm['planner.Course'])),
        ))
        db.send_create_signal('planner', ['Prereq'])

        # Adding field 'Requirement.force'
        db.add_column('planner_requirement', 'force', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Renaming column for 'Plan.start_year' to match new field type.
        db.rename_column('planner_plan', 'start_year_id', 'start_year')
        # Changing field 'Plan.start_year'
        db.alter_column('planner_plan', 'start_year', self.gf('django.db.models.fields.IntegerField')())

        # Removing index on 'Plan', fields ['start_year']
        db.delete_index('planner_plan', ['start_year_id'])

        # Adding field 'Enrollment.term'
        db.add_column('planner_enrollment', 'term', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['planner.Term']), keep_default=False)

        # Adding field 'Enrollment.year'
        db.add_column('planner_enrollment', 'year', self.gf('django.db.models.fields.IntegerField')(default=2012), keep_default=False)

        # Adding unique constraint on 'Enrollment', fields ['course', 'term', 'plan', 'year']
        db.create_unique('planner_enrollment', ['course_id', 'term_id', 'plan_id', 'year'])
    
    
    def backwards(self, orm):
        
        # Adding model 'Year'
        db.create_table('planner_year', (
            ('start_num', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['Year'])

        # Deleting model 'Prereq'
        db.delete_table('planner_prereq')

        # Deleting field 'Requirement.force'
        db.delete_column('planner_requirement', 'force')

        # Renaming column for 'Plan.start_year' to match new field type.
        db.rename_column('planner_plan', 'start_year', 'start_year_id')
        # Changing field 'Plan.start_year'
        db.alter_column('planner_plan', 'start_year_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Year']))

        # Adding index on 'Plan', fields ['start_year']
        db.create_index('planner_plan', ['start_year_id'])

        # Deleting field 'Enrollment.term'
        db.delete_column('planner_enrollment', 'term_id')

        # Deleting field 'Enrollment.year'
        db.delete_column('planner_enrollment', 'year')

        # Removing unique constraint on 'Enrollment', fields ['course', 'term', 'plan', 'year']
        db.delete_unique('planner_enrollment', ['course_id', 'term_id', 'plan_id', 'year'])
    
    
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'max_units': ('django.db.models.fields.IntegerField', [], {}),
            'min_units': ('django.db.models.fields.IntegerField', [], {}),
            'prereqs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['planner.Course']", 'null': 'True', 'through': "orm['planner.Prereq']", 'symmetrical': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['planner.Tag']", 'through': "orm['planner.TagMapping']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'planner.courseoffering': {
            'Meta': {'unique_together': "(('course', 'year', 'term', 'weekdays', 'start_time'),)", 'object_name': 'CourseOffering'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Course']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 50)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Instructor']", 'null': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 0)'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Term']"}),
            'weekdays': ('django.db.models.fields.CharField', [], {'default': "'MWF'", 'max_length': '5'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
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
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'planner.instructor': {
            'Meta': {'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Instructor'},
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
            'start_year': ('django.db.models.fields.IntegerField', [], {}),
            'student_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'university': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['planner.University']", 'unique': 'True'})
        },
        'planner.prereq': {
            'Meta': {'object_name': 'Prereq'},
            'for_course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'for'", 'to': "orm['planner.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandatory': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'prereq': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prereq'", 'to': "orm['planner.Course']"})
        },
        'planner.requirement': {
            'Meta': {'object_name': 'Requirement'},
            'force': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Tag']"})
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
        }
    }
    
    complete_apps = ['planner']
