from django.db import models
from django.contrib.auth.models import User
import datetime

TRIMESTER = 0
SEMESTER = 1

class Major(models.Model):
    name = models.CharField(max_length=128)
    tracks = models.ManyToManyField('RequirementGroup', related_name='tracks')
    
    def __unicode__(self):
        return self.name
class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        unique_together=('first_name', 'last_name')

    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)
        
    def natural_key(self):
        return "%s, %s" % (self.last_name, self.first_name) 

class University(models.Model):
    name = models.CharField(max_length=256)
    max_units_per_quarter = models.IntegerField(default=20)
    min_units = models.IntegerField(default=180)
    quarter_type = models.IntegerField(default=TRIMESTER)
    
    def __unicode__(self):
        return self.name

class Term(models.Model):
    num = models.IntegerField(primary_key=True)
    
    def __unicode__(self):
        if self.num == 0:
            return 'Autumn'
        elif self.num == 1:
            return 'Winter'
        elif self.num == 2:
            return 'Spring'
        elif self.num == 3:
            return 'Summer'
        else:
            return 'Unknown'

class Tag(models.Model):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name

class Course(models.Model):
    identifier = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    code = models.IntegerField()
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    class_number = models.IntegerField()
    max_units = models.IntegerField()
    min_units = models.IntegerField()
    tags = models.ManyToManyField(Tag, through='TagMapping')

    def __unicode__(self):
        return self.identifier

class RequirementGroup(models.Model):
    is_track = models.BooleanField(default=False)
    major = models.ForeignKey(Major, null=True, blank=True)
    name = models.CharField(max_length=64)
    n_reqs = models.IntegerField() #gonna change the name of this
     
    def __unicode__(self):
        return  self.name 
        
    def natural_key(self):
        return self.name
 
class Requirement(models.Model):
    name = models.CharField(max_length=64)
    fulfillers = models.ForeignKey(Tag)
    n_class = models.IntegerField();
    group = models.ForeignKey(RequirementGroup)
    bypassable = models.BooleanField(default=True)
    exclusive = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

#through class for many to many, will change
class TagMapping(models.Model):
    tag = models.ForeignKey(Tag)
    course = models.ForeignKey(Course)
    def __unicode__(self):
        return self.tag.__unicode__() + ", " + self.course.identifier

class PrereqGroup(models.Model):
    for_course = models.ForeignKey(Course, related_name='prereqs')
    mandatory = models.BooleanField()
    satisfiers = models.ManyToManyField(Course)
    
    def __unicode__(self):
        return self.for_course.identifier

class Exemption(models.Model):
    course = models.ForeignKey(Course)
    mutex_req_fulfilled = models.ForeignKey(Requirement, null=True)
    def __unicode__(self):
        return self.course.__unicode__()

class Plan(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University)
    major = models.ForeignKey(Major)
    start_year = models.IntegerField()
    num_years = models.IntegerField(default=4)
    aps = models.ManyToManyField(Exemption)
    track = models.ForeignKey(RequirementGroup, null=True)
    
    def __unicode__(self):
        return self.name
        
class CourseOffering(models.Model):
    course = models.ForeignKey(Course)
    year = models.IntegerField()
    term   = models.ForeignKey(Term)
    start_time = models.TimeField(default=datetime.time(9,00))
    end_time = models.TimeField(default=datetime.time(9,50))
    weekdays = models.CharField(max_length=5,default="MWF")
    instructor = models.ForeignKey(Instructor, null=True, blank=True)
    ctype = models.IntegerField(default=1) #section or lecture
    #duration = models.IntegerField()
    class Meta:
        unique_together = ('course', 'year', 'term', 'weekdays', 'start_time')
        
    def __unicode__(self):
        return self.course.identifier + ' ' + self.term.__unicode__() + ' ' + str(self.year) + '-' + str(self.year + 1)

class Enrollment(models.Model):
    course = models.ForeignKey(CourseOffering)
    plan = models.ForeignKey(Plan)
    units = models.IntegerField()
    mutex_req_fulfilled = models.ForeignKey(Requirement, null=True)

    class Meta:
        pass
        #unique_together = ('plan', 'course')
        
    def __unicode__(self):
        return self.course.__unicode__() + ' ' + self.plan.__unicode__()
