from django.db import models
from django.contrib.auth.models import User
import datetime

#class Course(models.Model):
#    identifier = models.CharField(max_length=20) # i.e. CS 106A
#    name = models.CharField(max_length=50) #i.e. Programming Methodology
#    description = models.CharField(max_length=300)
#    units = models.IntegerField()
#    startTime = models.TimeField(default=datetime.time(9,0))
#    endTime = models.TimeField(default=datetime.time(9,50))
#    weekdays = models.CharField(max_length=5, default="MWF") # i.e. MWF, TR, MTWR, MTWRF
#    
#    def __unicode__(self):
#        return self.identifier

TRIMESTER = 0
SEMESTER = 1
class UserData(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=64)

class Major(models.Model):
    name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name
class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        unique_together=('first_name', 'last_name')

    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)

class University(models.Model):
    name = models.CharField(max_length=256)
    max_units_per_quarter = models.IntegerField(default=20)
    min_units_per_quarter = models.IntegerField(default=9)
    quarter_type = models.IntegerField(default=TRIMESTER)
    
    def __unicode__(self):
        return self.name

# sort of a dummy class, multiplexed, should 
# only ever be numberOfTermsPerYear of them
# TODO better naming logic
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

#underscore case for vars, as per python style guide
class Course(models.Model):
    identifier = models.CharField(max_length=100)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    class_number = models.IntegerField()
    max_units = models.IntegerField()
    min_units = models.IntegerField()
    tags = models.ManyToManyField(Tag, through='TagMapping')
    #prereqs = models.ManyToManyField('self', null=True, through='Prereq', symmetrical=False)
    #grading = models.IntegerField() #C/NC, P/F, ABCDF, etc
    #repeatable_for_credit = models.BooleanField()

    def __unicode__(self):
        return self.identifier

class RequirementGroup(models.Model):
    major = models.ForeignKey(Major, null=True)
    name = models.CharField(max_length=64)
    n_prereqs = models.IntegerField() #gonna change the name of this
     
    def __unicode__(self):
        return  self.name # i forget if python auto converts to string
 
class Requirement(models.Model):
    name = models.CharField(max_length=64)
    fulfillers = models.ForeignKey(Tag)
    n_class = models.IntegerField();
    group = models.ForeignKey(RequirementGroup)
    def __unicode__(self):
        return self.name + ", " + str(self.fulfillers) + ", " + str(self.n_class)

#through class for many to many, will change
class TagMapping(models.Model):
    tag = models.ForeignKey(Tag)
    course = models.ForeignKey(Course)

class PrereqGroup(models.Model):
    for_course = models.ForeignKey(Course, related_name='prereqs')
    mandatory = models.BooleanField()
    satisfiers = models.ManyToManyField(Course)

class Plan(models.Model):
    student_name = models.CharField(max_length=100) #eventually user
    user = models.ForeignKey(UserData, null=True)
    university = models.OneToOneField(University)
    major = models.ForeignKey(Major)
    start_year = models.IntegerField()
    num_years = models.IntegerField(default=4)
    aps = models.ManyToManyField(Course)
    
    def __unicode__(self):
        return self.student_name
        
class CourseOffering(models.Model):
    course = models.ForeignKey(Course)
    year = models.IntegerField()
    term   = models.ForeignKey(Term)
    start_time = models.TimeField(default=datetime.time(9,00))
    end_time = models.TimeField(default=datetime.time(9,50))
    weekdays = models.CharField(max_length=5,default="MWF")
    instructor = models.ForeignKey(Instructor, null=True)
    ctype = models.IntegerField(default=1) #section or lecture
    #duration = models.IntegerField()
    class Meta:
        unique_together = ('course', 'year', 'term', 'weekdays', 'start_time')
        
    def __unicode__(self):
        return self.course.identifier + ' ' + self.term.__unicode__() + ' ' + str(self.year) + '-' + str(self.year + 1)

#does it scale
class Enrollment(models.Model):
    course = models.ForeignKey(CourseOffering)
    plan = models.ForeignKey(Plan)
    units = models.IntegerField()

    class Meta:
        pass
        #unique_together = ('plan', 'course')
        
    def __unicode__(self):
        return self.course.__unicode__() + ' ' + self.plan.__unicode__()

#through class for manyToMany, will change
class RequirementMapping(models.Model):
    coursereq = models.ForeignKey(Requirement, related_name="course_requirement")
    logreq = models.ForeignKey(Requirement, related_name="logical_requirement")

    def get_logreq(self):
        return 
