from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime 
# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class SemDetails(models.Model):
	sem_start = models.DateField(default = datetime.date(1900, 1, 1))
	sem_end = models.DateField(default = datetime.date(1900, 1, 1))
	user = models.OneToOneField(User, on_delete=models.CASCADE, null= True)
	

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null= True)
	test = models.CharField(max_length=200, default = "xyz") 

	def __str__(self):
		return self.user.username



class Subject(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	title = models.CharField(max_length = 200)
	percentage = models.FloatField(blank = True, default = 0)
	#color =  models.CharField(max_length = 200)
	# sub_type = models.CharField(max_length=50, null=True)

	def __str__(self):
		return self.title

class Timetable(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
	day = models.PositiveIntegerField(null=True,validators=[MinValueValidator(0), MaxValueValidator(6)])
	time = models.TimeField(blank=True)
	venue = models.CharField(max_length=200, default = "---") 

	
	period = models.IntegerField(null=True)
	value_int = models.IntegerField(default = -1)

	def __str__(self):
		return "Day: " + str(self.day) + " Period: " + str(self.period) + " --> " + str(self.subject)


class Attendance(models.Model):

	value = models.CharField(max_length=10)
	timetable = models.ForeignKey(Timetable,on_delete=models.CASCADE,null=True)
	Date = models.DateField()
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	value_int = models.IntegerField(default = -1)
	value_str = models.CharField(max_length=10, default= "Not Marked")

	def __str__(self):
		return str(self.Date) + " " + str(self.timetable.subject.title)





