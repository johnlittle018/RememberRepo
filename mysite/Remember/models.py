import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone

# Create your models here.

class Reminder(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    time = models.DateTimeField()
    reminder_text = models.CharField(max_length=200)

    def __str__(self):
        return '{}\'s reminder, time:{}'.format(self.patient, self.reminder_text)


class Patient(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    #find a patient's reminders by querying Reminder

    def __str__(self):
        return 'patient {}'.format(self.name)


class User(models.Model):
    patients = models.ManyToManyField(Patient, through='PatientClearanceAbstraction') #ManyToManyField helps manage queries
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return 'user {}'.format(self.name)


class PatientClearanceAbstraction(models.Model):
    user = models.ForeignKey(User)
    patient = models.ForeignKey(Patient)
    clearanceLevel = models.IntegerField(default=0) #can use BooleanField, but this allows room for functional expansion

    def __str__(self):
        return 'user {} has clearance {} with patient {}'.format(self.user, self.clearanceLevel, self.patient)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    picture = models.FileField(upload_to='uploads/images/', max_length=200) #https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.FileField
                                                                            #using FileField takes a little extra legwork comapred to CharField
                                                                            #upload_to can be set to any directory, and it can sort by upload date into subdirectories
                                                                            #also consider the ImageField datatype, which requires the Pillow library
    a1 = models.CharField(max_length=200)
    a2 = models.CharField(max_length=200)
    a3 = models.CharField(max_length=200)
    a4 = models.CharField(max_length=200)
    answer = models.IntegerField(default=0)
    lastSubAnswer = models.IntegerField(default=0)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return "%.25s" % '{}'.format(self.question_text) #first 25 characters of the question


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
    patient = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return '{}\'s quiz'.format(self.patient) #first 25 characters of the question
