from django.db import models
import datetime

class Course(models.Model):
    identifier = models.CharField(max_length=20) # i.e. CS 106A
    name = models.CharField(max_length=50) #i.e. Programming Methodology
    description = models.CharField(max_length=300)
    units = models.IntegerField()
    startTime = models.TimeField(default=datetime.time(9,0))
    endTime = models.TimeField(default=datetime.time(9,50))
    weekdays = models.CharField(max_length=5, default="MWF") # i.e. MWF, TR, MTWR, MTWRF
    
    def __unicode__(self):
        return self.identifier