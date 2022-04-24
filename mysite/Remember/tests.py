
from urllib import request
from django.test import TestCase

from .models import Patient, Reminder, User, PatientClearanceAbstraction, Result, Quiz, Question

def create_user(firstName, lastName, email):
    
    return User.objects.create(firstName=firstName, lastName=lastName, email=email)

def create_patient(firstName, lastName, email, samplePic):
    
    return Patient.objects.create(firstName=firstName, lastName=lastName, username=email, mugshot=samplePic)

class AdminTests(TestCase):
    def test_admin_create_new_patient(self):
        newAdmin = create_user(firstName='Hannah', lastName='Ilalokhoin', email='ilalokho012@email.com')

        newPatient = create_patient(firstName='Deborah', lastName='Ilalokhoin', email='ilalokho189@email.com', samplePic="/../../static/remember/images/questionImages/appa2.png")
        PatientClearanceAbstraction.objects.create(user=newAdmin, patient=newPatient, clearanceLevel = 2)

        admin = User.objects.get(pk = newAdmin.id)

        self.assertEqual(admin.patients.all().count(), 1)


    def test_admin_promote_admin(self):
        newAdmin = create_user(firstName='Hannah', lastName='Ilalokhoin', email='ilalokho012@email.com')
        
        newPatient = create_patient(firstName='Deborah', lastName='Ilalokhoin', email='ilalokho189@email.com', samplePic="/../../static/remember/images/questionImages/appa2.png")
        PatientClearanceAbstraction.objects.create(user=newAdmin, patient=newPatient, clearanceLevel = 2)

        admin = User.objects.get(pk = newAdmin.id)

        self.assertEqual(admin.patients.all().count(), 1)

    def test_add_admin_to_(self):
        newAdmin = create_user(firstName='Hannah', lastName='Ilalokhoin', email='ilalokho012@email.com')
        
        newPatient = create_patient(firstName='Deborah', lastName='Ilalokhoin', email='ilalokho189@email.com', samplePic="/../../static/remember/images/questionImages/appa2.png")
        PatientClearanceAbstraction.objects.create(user=newAdmin, patient=newPatient, clearanceLevel = 2)

        admin = User.objects.get(pk = newAdmin.id)

        self.assertEqual(admin.patients.all().count(), 1)


