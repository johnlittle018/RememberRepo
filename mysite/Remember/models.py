import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone

# Create your models here.


class Patient(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    mugshot = models.FileField(upload_to='uploads/images/patient_pics/', max_length=200, default="")
    #find a patient's reminders by querying Reminder

    def __str__(self):
        return 'patient {} {}'.format(self.firstName, self.lastName)

class Reminder(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    time = models.DateTimeField()
    reminder_text = models.CharField(max_length=200)

    def __str__(self):
        return '{}\'s reminder, time:{}'.format(self.patient, self.reminder_text)

class User(models.Model):
    patients = models.ManyToManyField(Patient, through='PatientClearanceAbstraction') #ManyToManyField helps manage queries
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    email = models.CharField(max_length=200)#it's functionally a username
    password = models.CharField(max_length=200)

    def __str__(self):
        return 'user {} {}'.format(self.firstName, self.lastName)


class PatientClearanceAbstraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clearanceLevel = models.IntegerField(default=0) #can use BooleanField, but this allows room for functional expansion

    def __str__(self):
        return 'user {} has clearance {} with patient {}'.format(self.user, self.clearanceLevel, self.patient)

class Result(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    timeStarted = models.DateTimeField()
    timeEnded = models.DateTimeField()
    timeElapsed = models.TimeField()
    totalQuestions = models.IntegerField(default=0)
    numCorrect = models.IntegerField(default=0)

    def __str__(self):
        return '{} completed at {}'.format(self.patient, self.timeEnded)

class Quiz(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, unique=False)
    order = models.IntegerField(default=0, unique=False)

    def __str__(self):
        return '{}\'s quiz'.format(self.patient) #first 25 characters of the question

class Question(models.Model):
    question_text = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=200, default="")
    picture = models.FileField(upload_to='uploads/images/question_pics/', max_length=200, default="") #https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.FileField
                                                                            #using FileField takes a little extra legwork comapred to CharField
                                                                            #upload_to can be set to any directory, and it can sort by upload date into subdirectories
                                                                            #also consider the ImageField datatype, which requires the Pillow library
    A = models.CharField(max_length=200, default="")
    B = models.CharField(max_length=200, default="")
    C = models.CharField(max_length=200, default="")
    D = models.CharField(max_length=200, default="")
    answer = models.IntegerField(default=0)
    lastSubAnswer = models.IntegerField(default=0)
    timeEnded = models.DateTimeField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%.25s" % '{}'.format(self.question_text) #first 25 characters of the question
