from django.db import models

class Course(models.Model):
    identifier = models.CharField(max_length=20) # i.e. CS 106A
    name = models.CharField(max_length=50) #i.e. Programming Methodology
    description = models.CharField(max_length=300)