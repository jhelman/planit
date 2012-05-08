# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Term'
        db.create_table('planner_term', (
            ('num', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['Term'])

        # Adding model 'DisjunctionRequirement'
        db.create_table('planner_disjunctionrequirement', (
            ('requirement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.Requirement'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('planner', ['DisjunctionRequirement'])

        # Adding model 'Plan'
        db.create_table('planner_plan', (
            ('student_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('university', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.University'], unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['Plan'])

        # Adding model 'Year'
        db.create_table('planner_year', (
            ('num', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Plan'])),
        ))
        db.send_create_signal('planner', ['Year'])

        # Adding model 'Enrollment'
        db.create_table('planner_enrollment', (
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Course'])),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Term'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Plan'])),
            ('year', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Year'])),
        ))
        db.send_create_signal('planner', ['Enrollment'])

        # Adding model 'RequirementMapping'
        db.create_table('planner_requirementmapping', (
            ('coursereq', self.gf('django.db.models.fields.related.ForeignKey')(related_name='course_requirement', to=orm['planner.Requirement'])),
            ('logreq', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logical_requirement', to=orm['planner.Requirement'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['RequirementMapping'])

        # Adding model 'TagMapping'
        db.create_table('planner_tagmapping', (
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Course'])),
            ('tag_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Tag'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['TagMapping'])

        # Adding model 'BreadthRequirement'
        db.create_table('planner_breadthrequirement', (
            ('min_courses', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('fulfillers', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Tag'])),
            ('requirement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.Requirement'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('planner', ['BreadthRequirement'])

        # Adding model 'University'
        db.create_table('planner_university', (
            ('max_units_per_quarter', self.gf('django.db.models.fields.IntegerField')(default=20)),
            ('quarter_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('planner', ['University'])

        # Adding model 'ConjunctionRequirement'
        db.create_table('planner_conjunctionrequirement', (
            ('requirement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.Requirement'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('planner', ['ConjunctionRequirement'])

        # Adding model 'DepthRequirement'
        db.create_table('planner_depthrequirement', (
            ('min_units', self.gf('django.db.models.fields.IntegerField')(default=15)),
            ('fulfillers', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Tag'])),
            ('requirement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.Requirement'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('planner', ['DepthRequirement'])

        # Adding model 'Tag'
        db.create_table('planner_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('planner', ['Tag'])

        # Adding model 'Instructor'
        db.create_table('planner_instructor', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['Instructor'])

        # Adding model 'Requirement'
        db.create_table('planner_requirement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('planner', ['Requirement'])

        # Deleting field 'Course.startTime'
        db.delete_column('planner_course', 'startTime')

        # Deleting field 'Course.endTime'
        db.delete_column('planner_course', 'endTime')

        # Adding field 'Course.instructor'
        db.add_column('planner_course', 'instructor', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['planner.Instructor']), keep_default=False)

        # Adding field 'Course.start_time'
        db.add_column('planner_course', 'start_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 50)), keep_default=False)

        # Adding field 'Course.end_time'
        db.add_column('planner_course', 'end_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 50)), keep_default=False)

        # Adding field 'Course.class_number'
        db.add_column('planner_course', 'class_number', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding M2M table for field offered on 'Course'
        db.create_table('planner_course_offered', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['planner.course'], null=False)),
            ('term', models.ForeignKey(orm['planner.term'], null=False))
        ))
        db.create_unique('planner_course_offered', ['course_id', 'term_id'])

        # Changing field 'Course.description'
        db.alter_column('planner_course', 'description', self.gf('django.db.models.fields.CharField')(max_length=1000))

        # Changing field 'Course.identifier'
        db.alter_column('planner_course', 'identifier', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Course.name'
        db.alter_column('planner_course', 'name', self.gf('django.db.models.fields.CharField')(max_length=64))
    
    
    def backwards(self, orm):
        
        # Deleting model 'Term'
        db.delete_table('planner_term')

        # Deleting model 'DisjunctionRequirement'
        db.delete_table('planner_disjunctionrequirement')

        # Deleting model 'Plan'
        db.delete_table('planner_plan')

        # Deleting model 'Year'
        db.delete_table('planner_year')

        # Deleting model 'Enrollment'
        db.delete_table('planner_enrollment')

        # Deleting model 'RequirementMapping'
        db.delete_table('planner_requirementmapping')

        # Deleting model 'TagMapping'
        db.delete_table('planner_tagmapping')

        # Deleting model 'BreadthRequirement'
        db.delete_table('planner_breadthrequirement')

        # Deleting model 'University'
        db.delete_table('planner_university')

        # Deleting model 'ConjunctionRequirement'
        db.delete_table('planner_conjunctionrequirement')

        # Deleting model 'DepthRequirement'
        db.delete_table('planner_depthrequirement')

        # Deleting model 'Tag'
        db.delete_table('planner_tag')

        # Deleting model 'Instructor'
        db.delete_table('planner_instructor')

        # Deleting model 'Requirement'
        db.delete_table('planner_requirement')

        # Adding field 'Course.startTime'
        db.add_column('planner_course', 'startTime', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 0)), keep_default=False)

        # Adding field 'Course.endTime'
        db.add_column('planner_course', 'endTime', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 50)), keep_default=False)

        # Deleting field 'Course.instructor'
        db.delete_column('planner_course', 'instructor_id')

        # Deleting field 'Course.start_time'
        db.delete_column('planner_course', 'start_time')

        # Deleting field 'Course.end_time'
        db.delete_column('planner_course', 'end_time')

        # Deleting field 'Course.class_number'
        db.delete_column('planner_course', 'class_number')

        # Removing M2M table for field offered on 'Course'
        db.delete_table('planner_course_offered')

        # Changing field 'Course.description'
        db.alter_column('planner_course', 'description', self.gf('django.db.models.fields.CharField')(max_length=300))

        # Changing field 'Course.identifier'
        db.alter_column('planner_course', 'identifier', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Course.name'
        db.alter_column('planner_course', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))
    
    
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
            'end_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 50)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Instructor']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'offered': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['planner.Term']", 'symmetrical': 'False'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 50)'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['planner.Tag']", 'through': "orm['planner.TagMapping']", 'symmetrical': 'False'}),
            'units': ('django.db.models.fields.IntegerField', [], {}),
            'weekdays': ('django.db.models.fields.CharField', [], {'default': "'MWF'", 'max_length': '5'})
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
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Course']"}),
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
        'planner.plan': {
            'Meta': {'object_name': 'Plan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Plan']"})
        }
    }
    
    complete_apps = ['planner']
