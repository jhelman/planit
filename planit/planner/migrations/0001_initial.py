# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Major'
        db.create_table('planner_major', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('planner', ['Major'])

        # Adding model 'Instructor'
        db.create_table('planner_instructor', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['Instructor'])

        # Adding unique constraint on 'Instructor', fields ['first_name', 'last_name']
        db.create_unique('planner_instructor', ['first_name', 'last_name'])

        # Adding model 'University'
        db.create_table('planner_university', (
            ('max_units_per_quarter', self.gf('django.db.models.fields.IntegerField')(default=20)),
            ('quarter_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('planner', ['University'])

        # Adding model 'Term'
        db.create_table('planner_term', (
            ('num', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['Term'])

        # Adding model 'Tag'
        db.create_table('planner_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('planner', ['Tag'])

        # Adding model 'Course'
        db.create_table('planner_course', (
            ('max_units', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('min_units', self.gf('django.db.models.fields.IntegerField')()),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('class_number', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['Course'])

        # Adding model 'Requirement'
        db.create_table('planner_requirement', (
            ('major', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Major'], null=True)),
            ('force', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['Requirement'])

        # Adding model 'DepthRequirement'
        db.create_table('planner_depthrequirement', (
            ('min_units', self.gf('django.db.models.fields.IntegerField')(default=15)),
            ('fulfillers', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Tag'])),
            ('requirement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.Requirement'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('planner', ['DepthRequirement'])

        # Adding model 'BreadthRequirement'
        db.create_table('planner_breadthrequirement', (
            ('min_courses', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('fulfillers', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Tag'])),
            ('requirement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.Requirement'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('planner', ['BreadthRequirement'])

        # Adding model 'TagMapping'
        db.create_table('planner_tagmapping', (
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Course'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Tag'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['TagMapping'])

        # Adding model 'Prereq'
        db.create_table('planner_prereq', (
            ('prereq', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prereq', to=orm['planner.Course'])),
            ('mandatory', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='for', to=orm['planner.Course'])),
        ))
        db.send_create_signal('planner', ['Prereq'])

        # Adding model 'Plan'
        db.create_table('planner_plan', (
            ('start_year', self.gf('django.db.models.fields.IntegerField')()),
            ('university', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.University'], unique=True)),
            ('major', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Major'])),
            ('student_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_years', self.gf('django.db.models.fields.IntegerField')(default=4)),
        ))
        db.send_create_signal('planner', ['Plan'])

        # Adding model 'CourseOffering'
        db.create_table('planner_courseoffering', (
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Term'])),
            ('start_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 0))),
            ('weekdays', self.gf('django.db.models.fields.CharField')(default='MWF', max_length=5)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Course'])),
            ('end_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 50))),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('instructor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Instructor'], null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['CourseOffering'])

        # Adding unique constraint on 'CourseOffering', fields ['course', 'year', 'term', 'weekdays', 'start_time']
        db.create_unique('planner_courseoffering', ['course_id', 'year', 'term_id', 'weekdays', 'start_time'])

        # Adding model 'Enrollment'
        db.create_table('planner_enrollment', (
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.CourseOffering'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Plan'])),
        ))
        db.send_create_signal('planner', ['Enrollment'])

        # Adding unique constraint on 'Enrollment', fields ['plan', 'course']
        db.create_unique('planner_enrollment', ['plan_id', 'course_id'])

        # Adding model 'ConjunctionRequirement'
        db.create_table('planner_conjunctionrequirement', (
            ('requirement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.Requirement'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('planner', ['ConjunctionRequirement'])

        # Adding model 'DisjunctionRequirement'
        db.create_table('planner_disjunctionrequirement', (
            ('requirement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.Requirement'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('planner', ['DisjunctionRequirement'])

        # Adding model 'RequirementMapping'
        db.create_table('planner_requirementmapping', (
            ('coursereq', self.gf('django.db.models.fields.related.ForeignKey')(related_name='course_requirement', to=orm['planner.Requirement'])),
            ('logreq', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logical_requirement', to=orm['planner.Requirement'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['RequirementMapping'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Major'
        db.delete_table('planner_major')

        # Deleting model 'Instructor'
        db.delete_table('planner_instructor')

        # Removing unique constraint on 'Instructor', fields ['first_name', 'last_name']
        db.delete_unique('planner_instructor', ['first_name', 'last_name'])

        # Deleting model 'University'
        db.delete_table('planner_university')

        # Deleting model 'Term'
        db.delete_table('planner_term')

        # Deleting model 'Tag'
        db.delete_table('planner_tag')

        # Deleting model 'Course'
        db.delete_table('planner_course')

        # Deleting model 'Requirement'
        db.delete_table('planner_requirement')

        # Deleting model 'DepthRequirement'
        db.delete_table('planner_depthrequirement')

        # Deleting model 'BreadthRequirement'
        db.delete_table('planner_breadthrequirement')

        # Deleting model 'TagMapping'
        db.delete_table('planner_tagmapping')

        # Deleting model 'Prereq'
        db.delete_table('planner_prereq')

        # Deleting model 'Plan'
        db.delete_table('planner_plan')

        # Deleting model 'CourseOffering'
        db.delete_table('planner_courseoffering')

        # Removing unique constraint on 'CourseOffering', fields ['course', 'year', 'term', 'weekdays', 'start_time']
        db.delete_unique('planner_courseoffering', ['course_id', 'year', 'term_id', 'weekdays', 'start_time'])

        # Deleting model 'Enrollment'
        db.delete_table('planner_enrollment')

        # Removing unique constraint on 'Enrollment', fields ['plan', 'course']
        db.delete_unique('planner_enrollment', ['plan_id', 'course_id'])

        # Deleting model 'ConjunctionRequirement'
        db.delete_table('planner_conjunctionrequirement')

        # Deleting model 'DisjunctionRequirement'
        db.delete_table('planner_disjunctionrequirement')

        # Deleting model 'RequirementMapping'
        db.delete_table('planner_requirementmapping')
    
    
    models = {
        'planner.breadthrequirement': {
            'Meta': {'object_name': 'BreadthRequirement'},
            'fulfillers': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Tag']"}),
            'min_courses': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'requirement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['planner.Requirement']", 'unique': 'True', 'primary_key': 'True'})
        },
        'planner.conjunctionrequirement': {
            'Meta': {'object_name': 'ConjunctionRequirement'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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
            'Meta': {'object_name': 'DisjunctionRequirement'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'requirement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['planner.Requirement']", 'unique': 'True', 'primary_key': 'True'})
        },
        'planner.enrollment': {
            'Meta': {'unique_together': "(('plan', 'course'),)", 'object_name': 'Enrollment'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.CourseOffering']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Plan']"})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Major']", 'null': 'True'})
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
            'num': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
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
