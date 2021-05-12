from djongo import models
from django.utils.timezone import now

# Create your models here.

class Push_model(models.Model):
	author=models.CharField(max_length=100)
	to_branch=models.CharField(max_length=100)
	time_stamp=models.DateTimeField(default=now,blank=False)

class Pull_model(models.Model):
	author=models.CharField(max_length=100)
	from_branch=models.CharField(max_length=100)
	to_branch=models.CharField(max_length=100)
	time_stamp=models.DateTimeField(default=now,blank=False)

class Merged_model(models.Model):
	author=models.CharField(max_length=100)
	from_branch=models.CharField(max_length=100)
	to_branch=models.CharField(max_length=100)
	time_stamp=models.DateTimeField(default=now,blank=False)