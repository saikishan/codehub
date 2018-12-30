from django.db import models
from codingcenter.scraper_config import SUPPORTED_PLATFORMS
# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length= 30)
    url = models.CharField(max_length= 100, unique= True)
    platform = models.CharField(max_length=5, choices= SUPPORTED_PLATFORMS)

class Assignment(models.Model):
    title = models.CharField(max_length=20)
    owner = models.CharField(max_length=30)
    questions = models.ManyToManyField(Question)
