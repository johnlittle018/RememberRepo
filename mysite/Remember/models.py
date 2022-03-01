import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone
#from django_cryptography.fields import encrypt


# Create your models here.


class Patient(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    mugshot = models.FileField(upload_to='uploads/images/patient_pics/', max_length=200, default="")
    #find a patient's reminders by querying Reminder

    def __str__(self):
        return 'patient {}'.format(self.name)

class Reminder(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    time = models.DateTimeField()
    reminder_text = models.CharField(max_length=200)

    def __str__(self):
        return '{}\'s reminder, time:{}'.format(self.patient, self.reminder_text)

class User(models.Model):
    patients = models.ManyToManyField(Patient, through='PatientClearanceAbstraction') #ManyToManyField helps manage queries
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)#it's functionally a username
    password = models.CharField(max_length=200)

    def __str__(self):
        return 'user {}'.format(self.name)


class PatientClearanceAbstraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clearanceLevel = models.IntegerField(default=0) #can use BooleanField, but this allows room for functional expansion

    def __str__(self):
        return 'user {} has clearance {} with patient {}'.format(self.user, self.clearanceLevel, self.patient)

class Quiz(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, unique=True)
    order = models.IntegerField(default=0, unique=True) # Jack requested this id to make routing easier

    def __str__(self):
        return '{}\'s quiz'.format(self.patient)

class Question(models.Model):
    question_text = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=200, default="")
    picture = models.FileField(upload_to='uploads/images/question_pics/', max_length=200, default="")
    #https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.FileField
    #using FileField takes a little extra legwork comapred to CharField
    #upload_to can be set to any directory, and it can sort by upload date into subdirectories
    #also consider the ImageField datatype, which requires the Pillow library
    A = models.CharField(max_length=200, default="")  #capital letters are a deliberate design decision for routing
    B = models.CharField(max_length=200, default="")  #capital letters are a deliberate design decision for routing
    C = models.CharField(max_length=200, default="")  #capital letters are a deliberate design decision for routing
    D = models.CharField(max_length=200, default="")  #capital letters are a deliberate design decision for routing
    answer = models.CharField(max_length=200, default="")
    lastSubAnswer = models.IntegerField(default=0)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return "%.25s" % '{}'.format(self.question_text) #first 25 characters of the question


class QuizResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    timeStarted = models.DateTimeField()
    timeEnded = models.DateTimeField()
    timeElapsed = models.TimeField()
    totalQuestions = models.IntegerField(default=0)
    numCorrect = models.IntegerField(default=0)
    # technically, I think it is improper to store totalQuestions and numCorrect when they could be
    # derived, but it will be more convenient than doing several queries every time we need them

    def __str__(self):
        return '{} completed at {}'.format(self.patient, self.timeEnded)


class QuestionResult(models.Model):
    # Every time a questionnaire is taken, a new QuizResult needs to be created first, followed by a QuestionResult
    # for each question answered. Each QuestionResult will be linked to a Question (so we know what the choices and
    # correct answer were at the time the questionnaire was taken) and a QuizResult (so we know exactly which
    # questionnaire it belongs to).
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quizResult = models.ForeignKey(QuizResult, on_delete=models.CASCADE)
    chosen_answer = models.IntegerField(default=0)
    # You'll have to query the database using the relationships between QuestionResult and Question and QuizResult
    # to determine whether the question was answered correctly. This means that every time a question is changed, a
    # new version needs to be created and the old one needs to be "disabled" (probably by nulling its Quiz
    # attribute) and stored for reference.