from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length= 30)
    url = models.CharField(max_length= 100, unique= True)
    created_by = models.ForeignKey('auth.User', related_name='questions', null=True,on_delete= models.SET_NULL)

class Assignment(models.Model):
    title = models.CharField(max_length=20)
    created_by = models.ForeignKey('auth.User',related_name= 'assignments', null=True, on_delete= models.SET_NULL)
    questions = models.ManyToManyField(Question)
    participant = models.ManyToManyField(User)