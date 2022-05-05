from django.urls import reverse
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Patient, User, PatientClearanceAbstraction, Result, Quiz, Question

class AdminTests(TestCase):
    
    @classmethod
    # sets up data for testing
    def setUpTestData(self):
        #set Cleint() method to self.client
        self.client = Client()
        #creates two admins
        self.client.post('/remember/createANewAdmin/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987', 'passwordConfirm':'Jupiter987', 
        'FName': 'Diana', 'LName' : 'Ilalokhoin'})

        #diana creates two patients
        self.client.get(reverse('Remember:createPatient'))
        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
           self.client.post('/remember/submitPatient/', {'uploadedPic': fp, 'email': 'ilalokho004@gannon.edu', 'password':'Jupiter987',
            'firstName': 'Cherry', 'lastName' : 'Ilalokhoin'})

        self.client.get(reverse('Remember:createPatient'))
        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
           self.client.post('/remember/submitPatient/', {'uploadedPic': fp, 'email': 'ilalokho123@gannon.edu', 'password':'Jupiter987',
            'firstName': 'Osamoje', 'lastName' : 'Ilalokhoin'})
            

        self.client.post('/remember/createANewAdmin/', {'Email': 'ilalokho006@gannon.edu', 'password': 'Jupiter987', 'passwordConfirm':'Jupiter987', 
        'FName': 'Linda', 'LName' : 'Ilalokhoin'})

        #creates  patient for Linda not Diana. Diana has no patient in this method
        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
           self.client.post('/remember/submitPatient/', {'uploadedPic': fp, 'email': 'ilalokho010@gannon.edu', 'password':'Jupiter987',
            'firstName': 'Oloho', 'lastName' : 'Ilalokhoin'})

          
        self.client.post('/remember/createANewAdmin/', {'Email': 'ilalokho534@gannon.edu', 'password': 'Jupiter987', 'passwordConfirm':'Jupiter987', 
        'FName': 'Nala', 'LName' : 'Ilalokhoin'})



#TestCase 1
    def test_login(self):
        response = self.client.post('/remember/login/', {'Email': 'ilalokho534@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/pickPatient/')
        admin = User.objects.get(email = 'ilalokho534@gannon.edu')

        self.assertEqual(admin.patients.all().count(), 0)

#TestCase 1-error
    def test_wrong_login(self):
        response = self.client.post('/remember/login/', {'Email': 'ilalokho003@gannon.edu', 'password': 'WrongPassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have entered the wrong username or password, please try again", html=True)

#TestCase 2
    def test_create_admin(self):
        response = self.client.post('/remember/createANewAdmin/', {'Email': 'ilalokho456@gannon.edu', 'password': 'Jupiter987', 'passwordConfirm':'Jupiter987', 
        'FName': 'Bella', 'LName' : 'Ilalokhoin'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/pickPatient/')
        admin = User.objects.get(email = 'ilalokho456@gannon.edu')

        self.assertEqual(admin.patients.all().count(), 0)


#TestCase 2- error
    def test_create_already_existing_user(self):
        response = self.client.post('/remember/createANewAdmin/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987', 'passwordConfirm':'Jupiter987', 
        'FName': 'Diana', 'LName' : 'Ilalokhoin'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The email you have entered is already in the system", html=True)

#TestCase 2-error2
    def test_create_admin_password_does_not_match(self):
        response = self.client.post('/remember/createANewAdmin/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987', 'passwordConfirm':'Jupiter9sxs987', 
        'FName': 'Diana', 'LName' : 'Ilalokhoin'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The passwords you entered did not match.", html=True)

#Testcase 3
    def test_admin_create_new_patient(self):
        response = self.client.post('/remember/login/', {'Email': 'ilalokho534@gannon.edu', 'password': 'Jupiter987'})
        self.assertRedirects(response, '/remember/pickPatient/')
        self.client.get(reverse('Remember:createPatient'))
        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
           self.client.post('/remember/submitPatient/', {'uploadedPic': fp, 'email': 'ilalokho019@gannon.edu', 'password':'Jupiter987',
            'firstName': 'Gary', 'lastName' : 'Ilalokhoin'})

        admin = User.objects.get(email = 'ilalokho534@gannon.edu')

        self.assertEqual(admin.patients.all().count(), 1)

        patientName = Patient.objects.filter(username = 'ilalokho019@gannon.edu')
        self.assertTrue(patientName)

#Testcase 3- error
    def test_admin_create_existing_patient(self):
        response = self.client.post('/remember/login/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987'})
        self.assertRedirects(response, '/remember/pickPatient/')
        self.client.get(reverse('Remember:createPatient'))
        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
            response = self.client.post('/remember/submitPatient/', {'uploadedPic': fp, 'email': 'ilalokho010@gannon.edu', 'password':'Jupiter987',
            'firstName': 'SpongeBob', 'lastName' : 'Ilalokhoin'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The email you have entered is already registered.", html=True)


#Testcase 4
    def test_admin_add_other_admin_to_patient(self):
        #admin logs in
        response = self.client.post('/remember/login/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/pickPatient/')

        #get url for pickPatient
        pickPatientResponse = self.client.get(reverse('Remember:pickPatient'))

        #checks to see if the two patients created exist
        self.assertTrue(b'<h5 class="names">Cherry</h5>' in pickPatientResponse.content)

        self.assertTrue(b'<h5 class="names">Osamoje</h5>' in pickPatientResponse.content)

        #choos one of the patients
        admin = User.objects.get(email = 'ilalokho003@gannon.edu')
        patient = Patient.objects.get(username = 'ilalokho004@gannon.edu')
        relation = PatientClearanceAbstraction.objects.get(user = admin, patient = patient)

        response = self.client.post('/remember/pickedPatient/', {'relation': relation.id})
        self.assertRedirects(response, '/remember/adminMenu/')

        adminResponse = self.client.get(response.url)
        self.assertTrue(b'<span>Admin Menu -</span>\n            <span>Cherry</span>' in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Edit Questionnaire</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Review Results</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">View Analytics</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Set Reminder</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Invite Admins</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Cherry\'s Account</h5>'in adminResponse.content)
         
        
        self.client.get(reverse('Remember:inviteAdmin'))
        response = self.client.post('/remember/processNewAdmin/', {'emailAddress': 'ilalokho500@gannon.edu', 'password': 'Jupiter987',
        'firstName': 'Patrick', 'lastName' : 'Ilalokhoin', 'CorI' : 'c'})
        self.assertContains(response, "You have successfully invited an Admin", html=True)

        newAdmin = User.objects.get(email = 'ilalokho500@gannon.edu')
        self.assertEqual(newAdmin.patients.all().count(), 1)



#Testcase 4-error
    def test_admin_add_another_admin_that_already_exists(self):
        #admin logs in
        response = self.client.post('/remember/login/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/pickPatient/')

        #get url for pickPatient
        pickPatientResponse = self.client.get(reverse('Remember:pickPatient'))

        #checks to see if the two patients created exist
        self.assertTrue(b'<h5 class="names">Cherry</h5>' in pickPatientResponse.content)


        #choose the patient
        admin = User.objects.get(email = 'ilalokho003@gannon.edu')
        patient = Patient.objects.get(username = 'ilalokho004@gannon.edu')
        relation = PatientClearanceAbstraction.objects.get(user = admin, patient = patient)

        response = self.client.post('/remember/pickedPatient/', {'relation': relation.id})
        self.assertRedirects(response, '/remember/adminMenu/')

        adminResponse = self.client.get(response.url)
        self.assertTrue(b'<span>Admin Menu -</span>\n            <span>Cherry</span>' in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Edit Questionnaire</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Review Results</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">View Analytics</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Set Reminder</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Invite Admins</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Cherry\'s Account</h5>'in adminResponse.content)
         
        
        self.client.get(reverse('Remember:inviteAdmin'))
        response = self.client.post('/remember/processNewAdmin/', {'emailAddress': 'ilalokho006@gannon.edu', 'password': 'Jupiter987',
        'firstName': 'Patrick', 'lastName' : 'Ilalokhoin', 'CorI' : 'c'})
        self.assertContains(response, "The email you have entered is already registered.", html=True)


#Testcase 5
    def test_admin_promotes_an_existing_user(self):
        #admin logs in
        response = self.client.post('/remember/login/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/pickPatient/')

        #get url for pickPatient
        pickPatientResponse = self.client.get(reverse('Remember:pickPatient'))

        #checks to see if the two patients created exist
        self.assertTrue(b'<h5 class="names">Cherry</h5>' in pickPatientResponse.content)


        #choose the patient
        admin = User.objects.get(email = 'ilalokho003@gannon.edu')
        patient = Patient.objects.get(username = 'ilalokho004@gannon.edu')
        relation = PatientClearanceAbstraction.objects.get(user = admin, patient = patient)

        response = self.client.post('/remember/pickedPatient/', {'relation': relation.id})
        self.assertRedirects(response, '/remember/adminMenu/')

        adminResponse = self.client.get(response.url)
        self.assertTrue(b'<span>Admin Menu -</span>\n            <span>Cherry</span>' in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Edit Questionnaire</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Review Results</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">View Analytics</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Set Reminder</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Invite Admins</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Cherry\'s Account</h5>'in adminResponse.content)
         
        
        self.client.get(reverse('Remember:inviteAdmin'))
        response = self.client.post('/remember/processNewAdmin/', {'emailAddress': 'ilalokho006@gannon.edu', 'password': '',
        'firstName': '', 'lastName' : '','CorI' : 'i'})
        self.assertContains(response, "You have successfully invited an Admin", html=True)

        existingAdmin = User.objects.get(email = 'ilalokho006@gannon.edu')

        check = PatientClearanceAbstraction.objects.get(user = existingAdmin, patient = patient)
        self.assertNotEqual(check, 0)


#Testcase 5-error
    def test_admin_promotes_a_nonexistent_user(self):
        #admin logs in
        response = self.client.post('/remember/login/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/pickPatient/')

        #get url for pickPatient
        pickPatientResponse = self.client.get(reverse('Remember:pickPatient'))

        #checks to see if the two patients created exist
        self.assertTrue(b'<h5 class="names">Cherry</h5>' in pickPatientResponse.content)


        #choose the patient
        admin = User.objects.get(email = 'ilalokho003@gannon.edu')
        patient = Patient.objects.get(username = 'ilalokho004@gannon.edu')
        relation = PatientClearanceAbstraction.objects.get(user = admin, patient = patient)

        response = self.client.post('/remember/pickedPatient/', {'relation': relation.id})
        self.assertRedirects(response, '/remember/adminMenu/')

        adminResponse = self.client.get(response.url)
        self.assertTrue(b'<span>Admin Menu -</span>\n            <span>Cherry</span>' in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Edit Questionnaire</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Review Results</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">View Analytics</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Set Reminder</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Invite Admins</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Cherry\'s Account</h5>'in adminResponse.content)
         
        
        self.client.get(reverse('Remember:inviteAdmin'))
        response = self.client.post('/remember/processNewAdmin/', {'emailAddress': 'non_existent_email@gannon.edu', 'password': '',
        'firstName': '', 'lastName' : '','CorI' : 'i'})
        self.assertContains(response, "The email you have entered is not registered.", html=True)


#Testcase 5-error2
    def test_admin_promotes_an_existing_admin(self):
        #admin logs in
        response = self.client.post('/remember/login/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/pickPatient/')

        #get url for pickPatient
        pickPatientResponse = self.client.get(reverse('Remember:pickPatient'))

        #checks to see if the two patients created exist
        self.assertTrue(b'<h5 class="names">Cherry</h5>' in pickPatientResponse.content)


        #choose the patient
        admin = User.objects.get(email = 'ilalokho003@gannon.edu')
        patient = Patient.objects.get(username = 'ilalokho004@gannon.edu')
        relation = PatientClearanceAbstraction.objects.get(user = admin, patient = patient)

        response = self.client.post('/remember/pickedPatient/', {'relation': relation.id})
        self.assertRedirects(response, '/remember/adminMenu/')

        adminResponse = self.client.get(response.url)
        self.assertTrue(b'<span>Admin Menu -</span>\n            <span>Cherry</span>' in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Edit Questionnaire</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Review Results</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">View Analytics</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Set Reminder</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Invite Admins</h5>'in adminResponse.content)
        self.assertTrue(b'<h5 class="names">Cherry\'s Account</h5>'in adminResponse.content)
         
        self.client.get(reverse('Remember:inviteAdmin'))
        response = self.client.post('/remember/processNewAdmin/', {'emailAddress': 'ilalokho500@gannon.edu', 'password': 'Jupiter987',
        'firstName': 'Patrick', 'lastName' : 'Ilalokhoin', 'CorI' : 'c'})
        self.assertContains(response, "You have successfully invited an Admin", html=True)

        newAdmin = User.objects.get(email = 'ilalokho500@gannon.edu')
        self.assertEqual(newAdmin.patients.all().count(), 1)
        
        self.client.get(reverse('Remember:inviteAdmin'))
        response = self.client.post('/remember/processNewAdmin/', {'emailAddress': 'ilalokho500@gannon.edu', 'password': '',
        'firstName': '', 'lastName' : '','CorI' : 'i'})
        self.assertContains(response, "The email you have entered is already an admin of this patient.", html=True)

# TestCase 6
    def test_admin_make_a_question(self):
        self.client = Client()
        # admin logs in
        response = self.client.post('/remember/login/', {'Email': 'ilalokho006@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/pickPatient/')

        #get url for pickPatient
        pickPatientResponse = self.client.get(reverse('Remember:pickPatient'))

        #checks to see if the two patients created exist
        self.assertTrue(b'<h5 class="names">Oloho</h5>' in pickPatientResponse.content)

        #choose the patient
        admin = User.objects.get(email = 'ilalokho006@gannon.edu')
        patient = Patient.objects.get(username = 'ilalokho010@gannon.edu')
        relation = PatientClearanceAbstraction.objects.get(user = admin, patient = patient)

        response = self.client.post('/remember/pickedPatient/', {'relation': relation.id})
        self.assertRedirects(response, '/remember/adminMenu/')
        self.client.get('/remember/editQuestionnaire/')

        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
           response = self.client.post('/remember/submitQuestion/', {'uploadedPic': fp, 'pDescription': 'This is your grandfather and he is so cool. You love him with all your heart', 'theQuestion':'Who is this guy',
            'answer1': 'Ben', 'answer2' : 'Garrett', 'answer3' : 'Andrew','answer4' : 'Jack', 'toggle' : 1})

        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
           response = self.client.post('/remember/submitQuestion/', {'uploadedPic': fp, 'pDescription': 'This is your mother and she is your whole life', 'theQuestion':'Who is this beautiful woman',
            'answer1': 'Andrew', 'answer2' : 'Garrett', 'answer3' : 'Daniella','answer4' : 'Jack', 'toggle' : 3})

        questionResponse = self.client.get(response.url)
        self.assertTrue(b'Question: Who is this guy'in questionResponse.content)
        self.assertTrue(b'Question: Who is this beautiful woman'in questionResponse.content)


class PatientTests(TestCase):
    
    @classmethod
    # sets up data for testing
    def setUpTestData(self):
        #set Cleint() method to self.client
        self.client = Client()

        self.client.post('/remember/createANewAdmin/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987', 'passwordConfirm':'Jupiter987', 
        'FName': 'Diana', 'LName' : 'Ilalokhoin'})

        #diana creates a patient
        self.client.get(reverse('Remember:createPatient'))
        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
           self.client.post('/remember/submitPatient/', {'uploadedPic': fp, 'email': 'ilalokho004@gannon.edu', 'password':'Jupiter987',
            'firstName': 'Cherry', 'lastName' : 'Ilalokhoin'})

        self.client.get(reverse('Remember:createPatient'))
        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
           self.client.post('/remember/submitPatient/', {'uploadedPic': fp, 'email': 'ilalokho123@gannon.edu', 'password':'Jupiter987',
            'firstName': 'Osamoje', 'lastName' : 'Ilalokhoin'})

        #choose the patient
        admin = User.objects.get(email = 'ilalokho003@gannon.edu')
        patient = Patient.objects.get(username = 'ilalokho004@gannon.edu')
        relation = PatientClearanceAbstraction.objects.get(user = admin, patient = patient)

        self.client.post('/remember/pickedPatient/', {'relation': relation.id})
        
        self.client.get('/remember/editQuestionnaire/')

        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
           self.client.post('/remember/submitQuestion/', {'uploadedPic': fp, 'pDescription': 'This is your grandfather and he is so cool. You love him with all your heart', 'theQuestion':'Who is this guy',
            'answer1': 'Ben', 'answer2' : 'Garrett', 'answer3' : 'Andrew','answer4' : 'Jack', 'toggle' : 1})

        with open('./Remember/static/remember/images/questionImages/2.jpg', 'rb') as fp:
           self.client.post('/remember/submitQuestion/', {'uploadedPic': fp, 'pDescription': 'This is your mother and she is your whole life', 'theQuestion':'Who is this beautiful woman',
            'answer1': 'Andrew', 'answer2' : 'Garrett', 'answer3' : 'Daniella','answer4' : 'Jack', 'toggle' : 3})

    def test_patient_answer_non_existing_question(self):
        #login as patient
        response = self.client.post('/remember/login/', {'Email': 'ilalokho123@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/patientMenu/')
        #take quiz
        response = self.client.get('/remember/takeQuestionnaire/')
        self.assertRedirects(response, '/remember/noQuestions/')

    def test_patient_answer_question(self):
        #login as patient
        response = self.client.post('/remember/login/', {'Email': 'ilalokho004@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/patientMenu/')
        #take quiz
        response = self.client.get('/remember/takeQuestionnaire/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/remember/answerQuestion/', {'toggle': 1})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/remember/answerQuestion/', {'toggle': 3})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/reviewResults/')

    def test_patient_review_results(self):
        #login as patient
        response = self.client.post('/remember/login/', {'Email': 'ilalokho004@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/patientMenu/')
        #take quiz
        response = self.client.get('/remember/takeQuestionnaire/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/remember/answerQuestion/', {'toggle': 1})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/remember/answerQuestion/', {'toggle': 3})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/reviewResults/')

        response = self.client.get('/remember/takeQuestionnaire/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/remember/answerQuestion/', {'toggle': 1})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/remember/answerQuestion/', {'toggle': 2})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/reviewResults/')


        resultResponse = self.client.get('/remember/reviewResults/')
        self.assertTrue(b'Questionnaire Results - Cherry' in resultResponse.content)

        patient = Patient.objects.get(username = 'ilalokho004@gannon.edu')
        completedQuizzes = Quiz.objects.filter(order = 2, patient = patient)

        self.assertEqual(completedQuizzes.all().count(), 2)

        questionnaireResultResponse = self.client.post('/remember/questionnaireResults/', {'quizID': completedQuizzes[1].id})

        self.assertTrue(b'Summary' in questionnaireResultResponse.content)
        self.assertTrue(b'Score' in questionnaireResultResponse.content)
        self.assertTrue(b'50.0%'in questionnaireResultResponse.content)


    def test_patient_view_scrapbook(self):
        #login as patient
        response = self.client.post('/remember/login/', {'Email': 'ilalokho004@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/patientMenu/')

        #view scrapbook
        response = self.client.get('/remember/scrapbook/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is your grandfather and he is so cool. You love him with all your heart", html=True)
        self.assertContains(response, "This is your mother and she is your whole life", html=True)


    def test_patient_results_reviewed_by_admin(self):
        #login as patient
        response = self.client.post('/remember/login/', {'Email': 'ilalokho004@gannon.edu', 'password': 'Jupiter987'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/patientMenu/')
        #patient take quiz
        response = self.client.get('/remember/takeQuestionnaire/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/remember/answerQuestion/', {'toggle': 1})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/remember/answerQuestion/', {'toggle': 3})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/reviewResults/')

        response = self.client.get('/remember/takeQuestionnaire/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/remember/answerQuestion/', {'toggle': 1})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/remember/answerQuestion/', {'toggle': 2})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/remember/reviewResults/')

        self.client.get('/remember/loginPage/')

        self.client.post('/remember/login/', {'Email': 'ilalokho003@gannon.edu', 'password': 'Jupiter987'})

        #choose the patient
        admin = User.objects.get(email = 'ilalokho003@gannon.edu')
        patient = Patient.objects.get(username = 'ilalokho004@gannon.edu')
        relation = PatientClearanceAbstraction.objects.get(user = admin, patient = patient)

        response = self.client.post('/remember/pickedPatient/', {'relation': relation.id})
        self.assertRedirects(response, '/remember/adminMenu/')

        resultResponse = self.client.get('/remember/reviewResults/')
        self.assertTrue(b'Questionnaire Results - Cherry' in resultResponse.content)

    
        completedQuizzes = Quiz.objects.filter(order = 2, patient = relation.patient)

        self.assertEqual(completedQuizzes.all().count(), 2)

        questionnaireResultResponse = self.client.post('/remember/questionnaireResults/', {'quizID': completedQuizzes[1].id})

        self.assertTrue(b'Summary' in questionnaireResultResponse.content)
        self.assertTrue(b'Score' in questionnaireResultResponse.content)
        self.assertTrue(b'50.0%'in questionnaireResultResponse.content)

        questionnaireResultResponse = self.client.post('/remember/questionnaireResults/', {'quizID': completedQuizzes[0].id})

        self.assertTrue(b'Summary' in questionnaireResultResponse.content)
        self.assertTrue(b'Score' in questionnaireResultResponse.content)
        self.assertTrue(b'100.0%'in questionnaireResultResponse.content)



class RememberUITestCases(TestCase):

    def test_make_admin_account_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'}, follow = True)
        code = response.status_code
        print(code)
        content = response.content
        self.assertRedirects(response, '/remember/pickPatient/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertTrue(b'Select a Patient' in response.content)
        self.assertTrue(b'form action="/remember/createPatient/" method="post"' in content)

        #print(content)


    def test_login_page_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})

        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow = True)
        code = response.status_code
        # print(code)
        content = response.content
        # print(content)
        self.assertRedirects(response, '/remember/pickPatient/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertTrue(b'Select a Patient' in response.content)
        self.assertTrue(b'form action="/remember/createPatient/" method="post"' in content)
        #print(content)

    def test_submit_patient_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})

        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow = True)
        with open('./Remember/static/remember/images/iphoneImg.jpg', 'rb') as fp:
            response = c.post('/remember/submitPatient/', {'email': 'astley@aol.com', 'password': 'nevergiveUup', 'passwordConfirm': 'nevergiveUup', 'firstName': 'Rick', 'lastName': 'Astley', 'uploadedPic': fp}, follow = True)
        code = response.status_code
        content = response.content
        # print(content)
        self.assertRedirects(response, '/remember/pickPatient/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertTrue(b'<h5 class="names">Rick</h5>' in content)
        self.assertTrue(b'iphoneImg.jpg' in content)

    def test_picked_patient_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})

        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow = True)
        with open('./Remember/static/remember/images/iphoneImg.jpg', 'rb') as fp:
            response = c.post('/remember/submitPatient/', {'email': 'astley@aol.com', 'password': 'nevergiveUup', 'passwordConfirm': 'nevergiveUup', 'firstName': 'Rick', 'lastName': 'Astley', 'uploadedPic': fp}, follow = True)
        response = c.post('/remember/pickedPatient/',
                          {'relation': '1'}, follow = True)
        code = response.status_code
        content = response.content
        self.assertRedirects(response, '/remember/adminMenu/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertTrue(b'<h5 class="names">Edit Questionnaire</h5>' in content)
        self.assertTrue(b'<h5 class="names">Review Results</h5>' in content)
        self.assertTrue(b'<h5 class="names">Set Reminder</h5>' in content)
        self.assertTrue(b'<h5 class="names">Rick\'s Account</h5>' in content)
        self.assertTrue(b'<h5 class="names">Invite Admins</h5>' in content)
        self.assertTrue(b'<span>Admin Menu -</span>' in content)
        self.assertTrue(b'<span>Rick</span>' in content)

    def test_submit_question_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})

        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow=True)
        with open('./Remember/static/remember/images/iphoneImg.jpg', 'rb') as fp:
            response = c.post('/remember/submitPatient/',
                              {'email': 'astley@aol.com', 'password': 'nevergiveUup', 'passwordConfirm': 'nevergiveUup',
                               'firstName': 'Rick', 'lastName': 'Astley', 'uploadedPic': fp}, follow=True)
        response = c.post('/remember/pickedPatient/',
                          {'relation': '1'}, follow=True)
        with open('./Remember/static/remember/images/RememberLogo.png', 'rb') as fp:
            response = c.post('/remember/submitQuestion/', {'uploadedPic': fp, 'pDescription': 'Do you Remember?',
                                                            'theQuestion': 'What is this logo?', 'answer1': 'ours',
                                                            'answer2': 'art', 'answer3': 'Fiverr Baybeee',
                                                            'answer4': 'nothing of note', 'toggle': 1}, follow=True)
        code = response.status_code
        content = response.content
        # print(content)
        self.assertRedirects(response, '/remember/editQuestionnaire/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertTrue(b'<p class="boxContent">' in content)
        self.assertTrue(b'Fiverr Baybeee' in content)
        self.assertTrue(b'ours' in content)
        self.assertTrue(b'art' in content)
        self.assertTrue(b'Questionnaire - Rick' in content)

    def test_login_page_patient_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})
        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow = True)
        with open('./Remember/static/remember/images/iphoneImg.jpg', 'rb') as fp:
            response = c.post('/remember/submitPatient/', {'email': 'astley@aol.com', 'password': 'nevergiveUup', 'passwordConfirm': 'nevergiveUup', 'firstName': 'Rick', 'lastName': 'Astley', 'uploadedPic': fp}, follow = True)
        response = c.post('/remember/login/', {'Email': 'astley@aol.com', 'password': 'nevergiveUup'}, follow=True)
        code = response.status_code
        content = response.content
        # print(content)
        self.assertRedirects(response, '/remember/patientMenu/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertTrue(b"Menu - Rick's" in content)
        self.assertTrue(b'<h5 class="names">Take Quiz</h5>' in content)

    def test_take_questionnaire_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})

        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow=True)
        with open('./Remember/static/remember/images/iphoneImg.jpg', 'rb') as fp:
            response = c.post('/remember/submitPatient/',
                              {'email': 'astley@aol.com', 'password': 'nevergiveUup', 'passwordConfirm': 'nevergiveUup',
                               'firstName': 'Rick', 'lastName': 'Astley', 'uploadedPic': fp}, follow=True)
        response = c.post('/remember/pickedPatient/',
                          {'relation': '1'}, follow=True)
        with open('./Remember/static/remember/images/RememberLogo.png', 'rb') as fp:
            response = c.post('/remember/submitQuestion/', {'uploadedPic': fp, 'pDescription': 'Do you Remember?',
                                                            'theQuestion': 'What is this logo?', 'answer1': 'ours',
                                                            'answer2': 'art', 'answer3': 'Fiverr Baybeee',
                                                            'answer4': 'nothing of note', 'toggle': 1}, follow=True)
        response = c.post('/remember/takeQuestionnaire/', follow=True)
        code = response.status_code
        content = response.content
        # print(content)
        self.assertTrue(code == 200)
        self.assertTrue(b'<button type="submit" value="1" class="btn btn-primary btn-lg customBtn" id="QuestionA"><h3>ours</h3></button>' in content)
        self.assertTrue(b'<div class="d-flex justify-content-center">' in content)

    def test_login_page_error_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})
        response = c.post('/remember/login/', {'Email': 'd001@gannon.edu', 'password': 'hi'}, follow = True)    #invalid email
        code = response.status_code
        content = response.content
        # print(content)
        self.assertTrue(code == 200)
        self.assertTrue(b"<strong>You have entered the wrong username or password, please try again</strong>" in content)
        self.assertTrue(b'Log in' in content)

    def test_submit_question_error_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})

        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow=True)
        with open('./Remember/static/remember/images/iphoneImg.jpg', 'rb') as fp:
            response = c.post('/remember/submitPatient/',
                              {'email': 'astley@aol.com', 'password': 'nevergiveUup', 'passwordConfirm': 'nevergiveUup',
                               'firstName': 'Rick', 'lastName': 'Astley', 'uploadedPic': fp}, follow=True)
        response = c.post('/remember/pickedPatient/',
                          {'relation': '1'}, follow=True)
        with open('./Remember/static/remember/images/RememberLogo.png', 'rb') as fp:
            response = c.post('/remember/submitQuestion/', {'uploadedPic': fp, 'pDescription': 'Do you Remember?',
                                                            'theQuestion': 'What is this logo?', 'answer1': 'ours',
                                                            'answer2': 'art', 'answer3': 'Fiverr Baybeee',
                                                            'answer4': '', 'toggle': 1}, follow=True)
        code = response.status_code
        content = response.content
        # print(content)
        self.assertTrue(code == 200)
        self.assertTrue(b'Questionnaire - Rick' in content)

    def test_edit_patient_email_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})

        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow=True)
        with open('./Remember/static/remember/images/iphoneImg.jpg', 'rb') as fp:
            response = c.post('/remember/submitPatient/',
                              {'email': 'astley@aol.com', 'password': 'nevergiveUup', 'passwordConfirm': 'nevergiveUup',
                               'firstName': 'Rick', 'lastName': 'Astley', 'uploadedPic': fp}, follow=True)
        response = c.post('/remember/pickedPatient/',
                          {'relation': '1'}, follow=True)
        response = c.post('/remember/managePatientEmail/',
                          {'updateType': 'email'}, follow=True)
        code = response.status_code
        content = response.content
        # print(content)
        #self.assertRedirects(response, '/remember/managePatientEmail/', status_code=302,
        #                     target_status_code=200, fetch_redirect_response=True)
        self.assertTrue(b'Hidden Password' in content)
        self.assertTrue(b'Rick' in content)
        self.assertTrue(b'Astley' in content)

    def test_edit_patient_password_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})

        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow=True)
        with open('./Remember/static/remember/images/iphoneImg.jpg', 'rb') as fp:
            response = c.post('/remember/submitPatient/',
                              {'email': 'astley@aol.com', 'password': 'nevergiveUup', 'passwordConfirm': 'nevergiveUup',
                               'firstName': 'Rick', 'lastName': 'Astley', 'uploadedPic': fp}, follow=True)
        response = c.post('/remember/pickedPatient/',
                          {'relation': '1'}, follow=True)
        response = c.post('/remember/managePatientPassword/',
                          {'updateType': 'password'}, follow=True)
        code = response.status_code
        content = response.content
        # print(content)
        # self.assertRedirects(response, '/remember/managePatientPassword/', status_code=302,
        #                      target_status_code=200, fetch_redirect_response=True)
        # self.assertTrue(b'astley @ aol.com>' in content)
        self.assertTrue(b'Rick' in content)
        self.assertTrue(b'Astley' in content)


    def test_edit_patient_pic_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})

        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow=True)
        with open('./Remember/static/remember/images/iphoneImg.jpg', 'rb') as fp:
            response = c.post('/remember/submitPatient/',
                              {'email': 'astley@aol.com', 'password': 'nevergiveUup', 'passwordConfirm': 'nevergiveUup',
                               'firstName': 'Rick', 'lastName': 'Astley', 'uploadedPic': fp}, follow=True)
        response = c.post('/remember/pickedPatient/',
                          {'relation': '1'}, follow=True)
        response = c.post('/remember/managePatientPic/',
                          {'updateType': 'pic'}, follow=True)
        code = response.status_code
        content = response.content
        # print(content)
        # self.assertRedirects(response, '/remember/managePatientPic/', status_code=302,
        #                      target_status_code=200, fetch_redirect_response=True)
        # self.assertTrue(b'astley@aol.com>' in content)
        self.assertTrue(b'Rick' in content)
        self.assertTrue(b'Astley' in content)
        self.assertTrue(b'Hidden Password' in content)

    def test_edit_patient_name_UI(self):
        c = Client()
        response = c.post('/remember/createANewAdmin/',
                          {'Email': 'didycz001@gannon.edu', 'password': 'hi', 'passwordConfirm': 'hi',
                           'FName': 'Andrew', 'LName': 'Didycz'})

        response = c.post('/remember/login/', {'Email': 'didycz001@gannon.edu', 'password': 'hi'}, follow=True)
        with open('./Remember/static/remember/images/iphoneImg.jpg', 'rb') as fp:
            response = c.post('/remember/submitPatient/',
                              {'email': 'astley@aol.com', 'password': 'nevergiveUup', 'passwordConfirm': 'nevergiveUup',
                               'firstName': 'Rick', 'lastName': 'Astley', 'uploadedPic': fp}, follow=True)
        response = c.post('/remember/pickedPatient/',
                          {'relation': '1'}, follow=True)
        response = c.post('/remember/managePatientName/',
                          {'updateType': 'name'}, follow=True)
        code = response.status_code
        content = response.content
        # print(content)
        # self.assertRedirects(response, '/remember/managePatientName/', status_code=302,
        #                      target_status_code=200, fetch_redirect_response=True)
        # self.assertTrue(b'astley@aol.com>' in content)
        self.assertTrue(b'Hidden Password' in content)
        self.assertTrue(b'Astley' in content)
        self.assertTrue(b'Rick' in content)