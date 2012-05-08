from django.db import models
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
class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)

class University(models.Model):
    name = models.CharField(max_length=256)
    max_units_per_quarter = models.IntegerField(default=20)
    quarter_type = models.IntegerField(default=TRIMESTER)

# sort of a dummy class, multiplexed, should 
# only ever be numberOfTermsPerYear of them
class Term(models.Model):
    num = models.IntegerField()

class Tag(models.Model):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name

#underscore case for vars, as per python style guide
class Course(models.Model):
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    class_number = models.IntegerField()
    units = models.IntegerField()
    instructor = models.ForeignKey(Instructor) #on per class atm
    offered = models.ManyToManyField(Term)
    weekdays = models.CharField(max_length=5,default="MWF")
    tags = models.ManyToManyField(Tag, through='TagMapping')
    #repeatable_for_credit = models.BooleanField()

    def __unicode__(self):
        return self.identifier

#add type field to avoid try catch when
#working with "upcasted" pointers
class Requirement(models.Model):
    pass

class CourseRequirement(Requirement):
    name = models.CharField(max_length=64)
    fulfillers = models.ForeignKey(Tag)
    class Meta:
        abstract = True

    def fulfilled_by(self):
        return [o.course for o in TagMapping.objects.filter(tag_name=self.fulfillers)]

    def req(self):
        return Requirement.objects.get(depthrequirement=self)

class DepthRequirement(CourseRequirement):
    min_units = models.IntegerField(default=15)
    def is_fulfilled(self, plan):
        taken = set(plan.courses_taken.all())
        req_opts = set(self.fulfilled_by())
        return sum(c.units for c in set(taken & req_opts)) >= self.min_units

    def __unicode__(self):
        return self.name

class BreadthRequirement(CourseRequirement):
    min_courses = models.IntegerField(default=4)

    def is_fulfilled(self, plan):
        taken = set(plan.courses_taken.all())
        req_opts = set(self.fulfilled_by())
        return len(taken & req_opts) >= self.min_courses

    def req(self):
        return Requirement.objects.get(depthrequirement=self)

    def __unicode__(self):
        return self.name

#through class for many to many, will change
class TagMapping(models.Model):
    tag_name = models.ForeignKey(Tag)
    course = models.ForeignKey(Course)

#could just as well be a string, but we may want
#to add additional info to the struct
class Major(models.Model):
    name = models.CharField(max_length=128)
    
class Plan(models.Model):
    student_name = models.CharField(max_length=100) #eventually user
    university = models.OneToOneField(University)
    major = models.ForeignKey(Major)

class Year(models.Model):
    num = models.IntegerField()
    plan = models.ForeignKey(Plan)

#does it scale
class Enrollment(models.Model):
    term = models.ForeignKey(Term)
    year = models.ForeignKey(Year)
    course = models.ForeignKey(Course)
    plan = models.ForeignKey(Plan)

    class Meta:
        unique_together = ('plan','term','year','course')

class CourseOffering(models.Model):
    course = models.ForeignKey(Course)
    term   = models.ForeignKey(Term)
    start_time = models.TimeField(default=datetime.time(9,50))
    end_time = models.TimeField(default=datetime.time(9,50))
    #duration = models.IntegerField()
    class Meta:
        unique_together = ('course', 'term', 'start_time')

class LogicalRequirement(Requirement):
    for_major = models.ForeignKey(Major)
    class Meta:
        abstract = True

    name = models.CharField(max_length=64)
    def fulfilled_by(self):
        courses = []
        for req in self.subrequirements():
            courses.extend(req.fulfilled_by())
        return courses

    #should be recursive
    def subrequirements(self):
        subreqs = []
        try:
            subreqs.extend([DepthRequirement.objects.get(requirement_ptr=o) for o in 
                RequirementMapping.objects.filter(logreq=self.req())])
        except Exception:
            pass
        try:
            subreqs.extend([BreadthRequirement.objects.get(requirement_ptr=o) for o in 
                RequirementMapping.objects.filter(logreq=self.req())])
        except Exception:
            pass

        return subreqs

class ConjunctionRequirement(Requirement):
    def is_fulfilled(self, plan):
        for req in self.reqs.all():
            if(not req.is_fulfilled(plan)):
                return False
        return True
 
    def req(self):
        return Requirement.objects.get(conjunctionrequirement=self)

    def __unicode__(self):
        return self.name

class DisjunctionRequirement(Requirement):
    def is_fulfilled(self, plan):
        for req in self.reqs.all():
            if(req.is_fulfilled(plan)):
                return True
        return False

    def req(self):
        return Requirement.objects.get(disjunctionrequirement=self)

    def __unicode__(self):
        return self.name

#through class for manyToMany, will change
class RequirementMapping(models.Model):
    coursereq = models.ForeignKey(Requirement, related_name="course_requirement")
    logreq = models.ForeignKey(Requirement, related_name="logical_requirement")

    def get_logreq(self):
        return 
