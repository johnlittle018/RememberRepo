from django.urls import reverse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Patient, Reminder, User, PatientClearanceAbstraction, Result, Quiz, Question

class AdminTests(TestCase):
      
    def test_admin_create_new_admin(self):
        response = self.client.post('/remember/createANewAdmin/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987', 'passwordConfirm':'Jupiter987', 
        'FName': 'Diana', 'LName' : 'Ilalokhoin'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/pickPatient/')
        admin = User.objects.get(email = 'ilalokho003@gannon.edu')

        self.assertEqual(admin.patients.all().count(), 0)

    def test_admin_create_new_patient(self):
        self.client.get(reverse('Remember:createPatient'))
        image = SimpleUploadedFile('image.jpg', b'file_content', content_type='image/jpg')
        self.client.post(reverse('Remember:submitPatient'), {'uploadedPic': image, 'email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987', 
        'firstName': 'Cherry', 'lastName' : 'Ilalokhoin'})
        

    # def test_admin_create_new_patient(self):
    #     newAdmin = create_user(firstName='Hannah', lastName='Ilalokhoin', email='ilalokho012@email.com')

    #     newPatient = create_patient(firstName='Deborah', lastName='Ilalokhoin', email='ilalokho189@email.com', samplePic="/../../static/remember/images/questionImages/appa2.png")
    #     PatientClearanceAbstraction.objects.create(user=newAdmin, patient=newPatient, clearanceLevel = 2)

    #     admin = User.objects.get(pk = newAdmin.id)

    #     self.assertEqual(admin.patients.all().count(), 1)





