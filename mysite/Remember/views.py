





import datetime
import email
import os
import time
from turtle import update
from urllib import request
import uuid
from django.http import Http404
from django.http import HttpResponse
from django.utils import timezone
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.views import generic
from django.urls import reverse
from sqlalchemy import null
from sympy import re
from django.core.files.storage import FileSystemStorage

#from mysite.polls.views import ResultsView



# importing models from our database. 
from .models import Patient, Reminder, User, PatientClearanceAbstraction, Result, Quiz, Question
# from .models import Choice, Question




### Stuff for everyone

#loads the login page
def loginPage(request):

    ## Clearing session data 
    request.session['loggedInID'] = 0
    request.session['userType'] = ""
    request.session['relationshipID'] = 0
    request.session['activeQuiz'] = 0
    request.session['activeQuestions'] = 0
    request.session['activeQuestionIndex'] = 0

    return render(request, 'Remember/loginPage.html')

# checks info from the login page
def login(request):

    print("This is the login function")

    #pulling email and password from the calling login form
    Email = request.POST['Email']
    userPassword = request.POST['password']

    # Checking our users
    if User.objects.filter(email = Email).exists():
        ourUser = User.objects.filter(email = Email)
        # print("email is in the system.")
        if ourUser[0].password == userPassword:
            # print("Password is good") 
            request.session['loggedInID'] = ourUser[0].id
            return HttpResponseRedirect(reverse('Remember:pickPatient'))
        
    
    # Checking our Patients
    if Patient.objects.filter(username = Email).exists():
        ourPatient = Patient.objects.filter(username = Email)
        # print("email is in the system.")
        if ourPatient[0].password == userPassword:
            # print("Password is good") 
            request.session['loggedInID'] = ourPatient[0].id
            request.session['userType'] = "patient"
            return HttpResponseRedirect(reverse('Remember:patientMenu'))
            
    
    # This is how we update the page with an error message
    return render(request, 'Remember/loginPage.html', 
    { 'error_message': "THis is dumy data",}
        )        


   

## if a user logs in, they must first pick a patient. 
def pickPatient(request):

    #pulling user from session data
    currentUser = User.objects.get(pk = request.session['loggedInID'])
    #pulling that users patient realations
    # .filter will always return a list, even if that list is empty, so be aware
    usersRelations = PatientClearanceAbstraction.objects.filter(user = currentUser)

    #pCA is short for Patient clearance Abstraction
    return render(request, 'Remember/pickPatient.html', {'pCA' : usersRelations})


## loads the createPatientPage
def createPatient(request):

    return render(request, 'Remember/adminEx/createPatient.html')

def createAdmin(request):

    
    return render(request, 'Remember/createAdmin.html')

## loads the help page
def helpPage(request):

    
    return render(request, 'Remember/helpPage.html')

def changePassword(request):

    
    return render(request, 'Remember/changePassword.html')


## Function for when a patient is picked
def pickedPatient(request):
    # prints all data passed from the form
    # print(request.POST.dict())

    ## pulling selected relation id from form
    relationID = request.POST['relation']

    ## pulling user from session data
    currentUser = User.objects.get(pk = request.session['loggedInID'])
    ## pulling relation from database using relation id
    userRelation = PatientClearanceAbstraction.objects.get(pk = relationID)

    ## the following checks that this is a valid user realtion for this user
    if userRelation.user.id != currentUser.id:
        ## If this runs the user is trying to accses another users relation, boots to login screen 
        ## where the current user is loged out
        print("security is trying to be broken, send back to login page")
        return loginPage(request)

    ## recording the relation in the session data
    request.session['relationshipID'] = userRelation.id

    ## this is where we check if we are relation 1 or 2 
    ## Relation 1 sends you to the family menu
    ## Relation 2 sends you to the admin menu
    ## in current build the family member relation is not supported
    if userRelation.clearanceLevel == 1:
        # print("This is a family member")
        request.session['userType'] = "familyMemeber"
        return familyMenu(request, userRelation.id)
    elif userRelation.clearanceLevel == 2:
        # print("This is an admin")
        request.session['userType'] = "admin"
        return HttpResponseRedirect(reverse('Remember:adminMenu'))

    ## below code should never run
    else:
        print("ERRRRROOORRR!!!!!!!!")

    return render(request, 'Remember/newPage.html')








## family and admin


## loads the make QuestionPage
def makeQuestion(request):

    ## pulling relation from session data
    myRelation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    # pulling the master quiz
    myQuiz = Quiz.objects.get(patient = myRelation.patient, order = 0)
    
    return render(request, 'Remember/makeQuestion.html' , {'userRelation' : myRelation, 'quize' : myQuiz})


## makes a new question
def submitQuestion(request):

    # pulling relation from session data
    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
    #pulling the master quiz
    myQuiz = Quiz.objects.get(patient = relation.patient, order = 0)

    ## stuff for images
    # pulling the picture from the form
    myThingy = request.FILES['uploadedPic']
    myFileSystem = FileSystemStorage()
    myFileSystem.save(myThingy.name, myThingy)
    source = "./media/" + myThingy.name 
    name = str(uuid.uuid4()) + myThingy.name
    destination = "./Remember/static/remember/images/questionImages/" + name 
    os.rename(source, destination)
    
    
    ## this is what is passed to the question for a refrence to the image.
    ## formated so it can be used directly in html
    nameForDatabase = "/../../static/remember/images/questionImages/" + name
 
    ## pulling data from the calling form
    photoDiscription = request.POST['pDescription']
    question = request.POST['theQuestion']
    answer1 = request.POST['answer1'] 
    answer2 = request.POST['answer2']
    answer3 = request.POST['answer3']
    answer4 = request.POST['answer4']
    correctAnswer = request.POST.get('toggle', null)
    
    # dummy date neded for the creation of a question
    fillerTimeEnded = datetime.date(2022, 2, 28)

    ## checking that the toggle has been selected
    if correctAnswer == null:
        ## to do
        ## code in error that pops up, at the moment it just breaks to newPage
        print("User did not click a correct answer")
        return render(request, 'Remember/newPage.html')
    else:
        #creating new question using form data
        newQuestion = Question(question_text=question, 
            description=photoDiscription, 
            picture=nameForDatabase, 
            A=answer1, 
            B=answer2, 
            C=answer3, 
            D=answer4, 
            answer=int(correctAnswer), 
            lastSubAnswer=0, 
            quiz=myQuiz, 
            timeEnded=fillerTimeEnded, 
            author=relation.user)
        # saving the new question 
        newQuestion.save()

    return HttpResponseRedirect(reverse('Remember:editQuestionnaire'))


    
## edit a question that already exsist
def resubmitQuestion(request):


    # pulling if of the question we want to edit from the calling form
    questionID = request.POST['question']
    
    #pulling relation from session data
    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
    myQuestion = Question.objects.get(pk = questionID)
    
    ## calling a function to check if this is a valid question to edit
    ## the user can edit the question id in chrom inspect, so we need to keep them in bounds
    canEdit = checkIfValidQuestionToEdit(relation, myQuestion)
    ## is this is not a valid question, send the user back to the login page.
    if canEdit == False: 
        return HttpResponseRedirect(reverse('Remember:loginPage'))


    ## stuff for images
    # pulling the picture from the form
    myThingy = request.FILES['uploadedPic']
    myFileSystem = FileSystemStorage()
    myFileSystem.save(myThingy.name, myThingy)
    source = "./media/" + myThingy.name 
    name = str(uuid.uuid4()) + myThingy.name
    destination = "./Remember/static/remember/images/questionImages/" + name 
    os.rename(source, destination)
    
    
    ## this is what is passed to the question for a refrence to the image.
    ## formated so it can be used directly in html
    nameForDatabase = "/../../static/remember/images/questionImages/" + name
 
    # pulling data from calling form
    photoDiscription = request.POST['pDescription']
    question = request.POST['theQuestion']
    answer1 = request.POST['answer1']
    answer2 = request.POST['answer2'] 
    answer3 = request.POST['answer3']
    answer4 = request.POST['answer4']
    correctAnswer = request.POST.get('toggle', null)

    ## should never be a problem, as editing a question will already have a selected anser.
    if correctAnswer == null:
        print("User did not click a correct answer")
        #todo, code in a page refresh error for such a senario
    else:
        # updating changes made to the question
        myQuestion.question_text = question
        myQuestion.description = photoDiscription
        myQuestion.A = answer1
        myQuestion.B = answer2
        myQuestion.C = answer3
        myQuestion.D = answer4
        myQuestion.answer = correctAnswer
        myQuestion.picture = nameForDatabase

        #saving the question changes
        myQuestion.save()

    return HttpResponseRedirect(reverse('Remember:editQuestionnaire'))


# function that takes a relation and a question
# reutrns true is the question is valid for editing, false if not 
def checkIfValidQuestionToEdit( relation, qestion):
    
    # pull quiz from database
    myQuiz = Quiz.objects.get(patient = relation.patient, order = 0)
    # pull questions from quiz 
    questions = Question.objects.filter(quiz = myQuiz)
    isValidQuestionToEdit = False
    # chekc if the question we are trying to edit is a question of the patient we have checked out
    for q in questions:
        if q.id == qestion.id:
            isValidQuestionToEdit = True
            break
    
    return isValidQuestionToEdit



## Removes a question from a quize
def removeQuestion(request):

    ## pull question id from the calling form
    questionID = request.POST['question']
    ## pulling relation from the session 
    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
    # pulling question fro the database using question id
    question = Question.objects.get(pk = questionID)

    # calling method to check if a valid question to modify
    isValidQuestionToEdit = checkIfValidQuestionToEdit(relation, question)

    if isValidQuestionToEdit == True:
        ## delete the question from the quiz and database
        question.delete()
        return HttpResponseRedirect(reverse('Remember:editQuestionnaire'))
    else:
        return HttpResponseRedirect(reverse('Remember:loginPage'))



## loads the edit questionaire page
def editQuestionnaire(request):

    # pulling the reation from the session data    
    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
    # pulling patients quize
    myQuiz = Quiz.objects.get(patient = relation.patient, order = 0)
   
    ## try to find questions of the quiz "may not be any", if not set to zero for later html logic
    try:
        myQuestions = Question.objects.filter(quiz = myQuiz)  
    except:
        myQuestions = 0

    return render(request, 'Remember/editQuestionnaire.html', {'userRelation' : relation, 'questions' : myQuestions})


## loads the edit question page
def editQuestion(request):
    
    #pulling the question to be edited.
    questionID = request.POST['question']
    # pulling the reation from the session data
    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
    # pulling the question from the database using quiestionID
    question = Question.objects.get(pk = questionID)
    
    # using function to check if this is a valid question to edit
    isValidQuestionToEdit = checkIfValidQuestionToEdit(relation, question)
            
    if isValidQuestionToEdit == True:
        return render(request, 'Remember/editQuestion.html', {'userRelation' : relation, 'question' : question})
    else:
        return HttpResponseRedirect(reverse('Remember:loginPage'))



    




## Patient and Admin


## loads the review results page
def reviewResults(request):

    ## both patients and admin can review the quiz results, data is loaded diffrently for both

    ## for patient
    if request.session['userType'] == "patient":
        # pulling patient from session
        user = Patient.objects.get(pk = request.session['loggedInID'])
        # pulling all completed quizes
        myQuizs = Quiz.objects.filter(order = 2, patient = user)

        ## the results of a quiz are never calculated and stored, each quiz is saved after competion, and reslts data is always calculated on request.
        ## saves on database storage and complexity, but makes getting thos results complicated and possibly slow

        # array for storing calculated results
        results = []
        
        # for each copleted quiz, put it in a results containter
        for quiz in myQuizs:
            results.append(ResultContainer(quiz))

        return render(request, 'Remember/reviewResults.html', {'QuizeResults': results, 'patient': user})

    # for amdin    
    elif request.session['userType'] == "admin":
        
        # pulling relation from sesion
        relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
        # pulling all completed quizes   
        myQuizs = Quiz.objects.filter(order = 2, patient = relation.patient)
        
        # array for storing calculated results
        results = []

        # for each copleted quiz, put it in a results containter
        for quiz in myQuizs:
            results.append(ResultContainer(quiz))

        results.reverse()

        return render(request, 'Remember/reviewResults.html', {'QuizeResults': results, 'patient': relation.patient})

    else:
        ## code should never run, but satifiys logic
        return HttpResponseRedirect(reverse('Remember:loginPage'))








## loads the page that shows the results for each quesiton in a quiz compleation
def questionnaireResults(request):
    
    # pulling quiz from requesting form
    myQuiz = Quiz.objects.get(pk = request.POST['quizID'])
    # throwing quiz in a results containter, calculates a bunch of usefull data
    myResult = ResultContainer(myQuiz)
    
    ## if user is a patient  
    if request.session['userType'] == "patient": 
        # pull patient from the session
        user = Patient.objects.get(pk = request.session['loggedInID'])
        # check that this quiz was comleated by the patient
        if myQuiz.patient != user: 
            return HttpResponseRedirect(reverse('Remember:loginPage'))

        return render(request, 'Remember/questionnaireResults.html', {'result' : myResult, 'questions' : myResult.myQuestions })
        
    ## if user is an admin
    elif request.session['userType'] == "admin":
        # pull Relation from the session
        relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
        # check that this quiz was comleated by the patient
        if myQuiz.patient != relation.patient: 
            return HttpResponseRedirect(reverse('Remember:loginPage'))
          
        return render(request, 'Remember/questionnaireResults.html', {'result' : myResult, 'questions' : myResult.myQuestions })


    # should never run
    return HttpResponseRedirect(reverse('Remember:loginPage'))
    
    


# function that takes a list of questions
# retuns a list of scores values
def calculateScore(questionsIn):
    correct = 0
    wrong = 0
    for question in questionsIn:
        if question.lastSubAnswer == question.answer:
            correct = correct + 1
        else:
            wrong = wrong + 1
         
    total = correct + wrong
    score = (correct / total) * 100
    tally = []
    tally.append(score)
    tally.append(correct)
    tally.append(wrong)
    return tally




## Throw a quize in, and this will provide you will all result atrubutes you would like to see.
## result atributes need to be calculated in this container, as they are not stored in the database.
class ResultContainer:
    def __init__(self, quizIn):
        self.quiz = quizIn
        self.myQuestions = Question.objects.filter(quiz = self.quiz) 
        self.length = len(self.myQuestions)
        self.completionTime = self.myQuestions[(self.length - 1)].timeEnded
        myTally = calculateScore(self.myQuestions)
        self.score = myTally[0]
        self.correct = myTally[1]
        self.wrong = myTally[2]
         


## Stuff exclusive to patient



# loads the scrapbook page
def scrapbook(request): 
    # loads patient data from session
    myPatient = Patient.objects.get(pk = request.session['loggedInID'])
    # pull current quiz from database
    myQuiz = Quiz.objects.filter(order = 0, patient = myPatient)
    # pulling questions from quiz
    myQuestions = Question.objects.filter(quiz = myQuiz)

    # if there are no current questions
    if len(myQuestions) == 0: 
        return HttpResponseRedirect(reverse('Remember:noQuestions'))

    return render(request, 'Remember/patientEx/scrapbook.html', {'questions': myQuestions })



# loads the no questions page
def noQuestions(request):

    return render(request, 'Remember/patientEx/noQuestions.html')

## loads the no quiz page
def noQuiz(request):

    return render(request, 'Remember/noQuiz.html')




## loads the take questionaire page
def takeQuestionnaire(request):
    # this is the method that will be called the first time a questionair is started, initlizes settup

    # loads the patient from session
    myPatient = Patient.objects.get(pk = request.session['loggedInID'])
    # pull current quiz
    myQuiz = Quiz.objects.get(patient = myPatient, order = 0)
    # pulls questions from the quiz
    myQuestions = Question.objects.filter(quiz = myQuiz)
    
    # if there are not questions, send to the no questions page
    if len(myQuestions) == 0:
        print("we should be redirected")
        return HttpResponseRedirect(reverse('Remember:noQuestions'))

    # creating a new quiz to store ansers 
    newQuiz = Quiz(patient=myQuiz.patient, order = 1)
    newQuiz.save()

    # stores question ids for us to later iterate through
    newQuestionIDs = []

    # duplicate each question, add it to the new quize and record its new id
    for question in myQuestions:
        newQuestion = Question(question_text=question.question_text,
         description=question.description,
         picture=question.picture,
         A=question.A,
         B=question.B,
         C=question.C,
         D=question.D,
         answer=question.answer,
         lastSubAnswer=question.lastSubAnswer,
         timeEnded=question.timeEnded,
         quiz = newQuiz,
         author=question.author)
        newQuestion.save()

        newQuestionIDs.append(newQuestion.id)

    # saving the following attributes with the session, used for iterating through questions in the quiz
    request.session['activeQuiz'] = newQuiz.id
    request.session['activeQuestions'] = newQuestionIDs
    request.session['activeQuestionIndex'] = 0
    

    return takeQuestion(request)
    

## this is called to load a question during the quize
def takeQuestion(request):

    ## pulling values from the session
    myQuestionsIDs = request.session['activeQuestions']
    myQuestionIndex = request.session['activeQuestionIndex'] 

    ## if we have answered all questions, mark the quiz as order 2 for compleation, redirect to review results
    if myQuestionIndex == len(myQuestionsIDs):
        myQuiz = Quiz.objects.get(pk = request.session['activeQuiz'])
        myQuiz.order = 2
        myQuiz.save()
        return HttpResponseRedirect(reverse('Remember:reviewResults'))
    else:
        # load the next question
        currentQuestion = Question.objects.get(pk = myQuestionsIDs[myQuestionIndex])
        return render(request, 'Remember/patientEx/takeQuestionnaire.html', {'question' : currentQuestion})

## called to answer a quesiton  
def answerQuestion(request):
    ## pulling values from the session
    myQuestionsIDs = request.session['activeQuestions']
    myQuestionIndex = request.session['activeQuestionIndex'] 
    # pulling the current question
    currentQuestion = Question.objects.get(pk = myQuestionsIDs[myQuestionIndex])
    
    # pulling the given answer from the calling form
    givenAnswer = int(request.POST.get('toggle', null))

    # if the given answer value is invalid, just reload this question
    if givenAnswer == null or givenAnswer < 1 or givenAnswer > 4 :
        return takeQuestion(request)
    
    ## save the anser given and the time it was completed in the database
    currentQuestion.lastSubAnswer = givenAnswer
    currentQuestion.timeEnded = datetime.datetime.now()
    currentQuestion.save()
    
    # increasing the question index
    myQuestionIndex = myQuestionIndex + 1; 
    request.session['activeQuestionIndex'] = myQuestionIndex

    ## load the next question
    return takeQuestion(request)


## loads view remider page
def viewReminder(request):
    
    
    return render(request, 'Remember/patientEx/viewReminder.html')


## loads the patient menu
def patientMenu(request):
    
    # pulling patient from session
    ourPatient = Patient.objects.get(pk = request.session['loggedInID'])

    return render(request, 'Remember/patientEx/patientMenu.html', {'patient' : ourPatient})




## Exclusive to Admin

## Loads the admin menu
def adminMenu(request):

    # pulling relation from session
    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    return render(request, 'Remember/adminEx/adminMenu.html', {'userRelation' : relation})

## Loads the graph data page
def graphsData(request):

    return render(request, 'Remember/adminEx/graphsData.html')

## loads the invite family page
def inviteFamily(request):

    return render(request, 'Remember/adminEx/inviteFamily.html')

# loads the invite admin page
def inviteAdmin(request):

    return render(request, 'Remember/adminEx/inviteAdmin.html')



## called when submitting a new admin account
def processNewAdmin(request):

    # pulling relation from session
    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    # pulling data from requesting forms
    email = request.POST['emailAddress']
    password = request.POST['password']
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    corI = request.POST['CorI']

    ## if conditional is true, we are adding an account that already exist.
    if corI == "i":
        
        ## see if that account exist, if not, throw to error page
            
        try:
            myNewAdmin = User.objects.get(email = email)
        except:
            ## user does not exist
            return render(request, 'Remember/adminEx/inviteAdmin.html', 
                { 'error_message': "The email you have entered is not registered.",}
            )       

        ## make sure this relation does not already exist
        
        check = PatientClearanceAbstraction.objects.filter(patient = relation.patient, user = myNewAdmin)

        if len(check) != 0:
            return render(request, 'Remember/adminEx/inviteAdmin.html', 
                { 'error_message': "The email you have entered already an admin of this patient.",}
            )
        

        myNewRelation = PatientClearanceAbstraction(user=myNewAdmin, patient=relation.patient, clearanceLevel = 2)
        myNewRelation.save()
            
        return render(request, 'Remember/adminEx/inviteAdmin.html', 
            { 'coi_message': "You have successfully invited an Admin",}
        )

       


        
    if password == '' or firstName == '' or lastName == '':    
        return render(request, 'Remember/adminEx/inviteAdmin.html', 
            { 'error_message': "Please enter data in all feilds.",}
        )


    check = User.objects.filter(email = email)

    if len(check) != 0:
        return render(request, 'Remember/adminEx/inviteAdmin.html', 
        { 'error_message': "The email you have entered is already registered.",}
        )         

    ## We are creating a user
    ## we are under the assumption that the all the feilds have been filed and cheked on the html side of things

    myNewAdmin = User(firstName=firstName, lastName=lastName, email=email, password=password)
    myNewAdmin.save()
    myNewRelation = PatientClearanceAbstraction(user=myNewAdmin, patient=relation.patient, clearanceLevel = 2)
    myNewRelation.save()

    return render(request, 'Remember/adminEx/inviteAdmin.html', 
            { 'coi_message': "You have successfully invited an Admin",}
        )



def userMenu(request):

    if request.session['userType'] == "patient":
        return HttpResponseRedirect(reverse('Remember:patientMenu'))

    if request.session['userType'] == "admin":
        return HttpResponseRedirect(reverse('Remember:adminMenu'))

    return HttpResponseRedirect(reverse('Remember:loginPage'))



def updateUser(request):
    
    
    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])    
    myPatient = relation.patient

    updateType = request.POST['updateType']


    if updateType == "email":
        email = request.POST['email']
        myPatient.username = email
        myPatient.save()
        return HttpResponseRedirect(reverse('Remember:userMenu'))
      

    if updateType == "password":
        passwordConfirm = request.POST['passwordConfirm']
        password = request.POST['password']
        if passwordConfirm == password:
            myPatient.password = password
            myPatient.save()
        else:
            return render(request, 'Remember/adminEx/managePatientPassword.html', 
            { 'error_message': "The passwords you entered did not match.", 'userRelation' : relation }
            )


        return HttpResponseRedirect(reverse('Remember:userMenu'))

    if updateType == "name":
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        myPatient.firstName = firstName
        myPatient.lastName = lastName
        myPatient.save()
        return HttpResponseRedirect(reverse('Remember:userMenu'))
        

    if updateType == "pic":
        ## stuff for images
        myThingy = request.FILES['uploadedPic']
        myFileSystem = FileSystemStorage()
        myFileSystem.save(myThingy.name, myThingy)
        source = "./media/" + myThingy.name 
        name = str(uuid.uuid4()) + myThingy.name
        destination = "./Remember/static/remember/images/questionImages/" + name 
        os.rename(source, destination)
        
        
        ## this is what is passed to the question for a refrence to the image.
        ## formated so it can be used directly in html
        nameForDatabase = "/../../static/remember/images/questionImages/" + name

        myPatient.mugshot = nameForDatabase
        myPatient.save()

        return HttpResponseRedirect(reverse('Remember:userMenu'))




    return HttpResponseRedirect(reverse('Remember:loginPage'))


    
    
    
    

    return HttpResponseRedirect(reverse('Remember:userMenu'))


def updatePatient(request):
    
    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])    
    myPatient = relation.patient

    updateType = request.POST['updateType']


    if updateType == "email":
        email = request.POST['email']
        myPatient.username = email
        myPatient.save()
        return HttpResponseRedirect(reverse('Remember:userMenu'))
      

    if updateType == "password":
        passwordConfirm = request.POST['passwordConfirm']
        password = request.POST['password']
        if passwordConfirm == password:
            myPatient.password = password
            myPatient.save()
        else:
            return render(request, 'Remember/adminEx/managePatientPassword.html', 
            { 'error_message': "The passwords you entered did not match.", 'userRelation' : relation }
            )


        return HttpResponseRedirect(reverse('Remember:userMenu'))

    if updateType == "name":
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        myPatient.firstName = firstName
        myPatient.lastName = lastName
        myPatient.save()
        return HttpResponseRedirect(reverse('Remember:userMenu'))
        

    if updateType == "pic":
        ## stuff for images
        myThingy = request.FILES['uploadedPic']
        myFileSystem = FileSystemStorage()
        myFileSystem.save(myThingy.name, myThingy)
        source = "./media/" + myThingy.name 
        name = str(uuid.uuid4()) + myThingy.name
        destination = "./Remember/static/remember/images/questionImages/" + name 
        os.rename(source, destination)
        
        
        ## this is what is passed to the question for a refrence to the image.
        ## formated so it can be used directly in html
        nameForDatabase = "/../../static/remember/images/questionImages/" + name

        myPatient.mugshot = nameForDatabase
        myPatient.save()

        return HttpResponseRedirect(reverse('Remember:userMenu'))




    return HttpResponseRedirect(reverse('Remember:loginPage'))




def managePatientAccount(request):

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    return render(request, 'Remember/adminEx/managePatientAccount.html', {'userRelation' : relation})

def managePatientPic(request):

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    return render(request, 'Remember/adminEx/managePatientPic.html', {'userRelation' : relation})

def managePatientEmail(request):

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    return render(request, 'Remember/adminEx/managePatientEmail.html', {'userRelation' : relation})

def managePatientPassword(request):

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    return render(request, 'Remember/adminEx/managePatientPassword.html', {'userRelation' : relation})

def managePatientName(request):

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    return render(request, 'Remember/adminEx/managePatientName.html', {'userRelation' : relation})







def manageMyAdminAccount(request):

    return render(request, 'Remember/adminEx/manageMyAdminAccount.html', {'userRelation' : relation})

def manageMyAdminEmail(request):

    return render(request, 'Remember/adminEx/manageMyAdminEmail.html', {'userRelation' : relation})

def manageMyAdminPassword(request):

    return render(request, 'Remember/adminEx/manageMyAdminPassword.html', {'userRelation' : relation})

def manageMyAdminName(request):

    return render(request, 'Remember/adminEx/manageMyAdminName.html', {'userRelation' : relation})



# loads noUser Page
def noUser(request):

    return render(request, 'Remember/noUser.html')

# lods the New admin page
def newAdmin(request):

    return render(request, 'Remember/newAdmin.html')


## called when making a new patient acount
def submitPatient(request):

    ## loading the user from session
    myUser = User.objects.get(pk = request.session['loggedInID'])

    ## stuff for images
    myThingy = request.FILES['uploadedPic']
    myFileSystem = FileSystemStorage()
    myFileSystem.save(myThingy.name, myThingy)
    source = "./media/" + myThingy.name 
    name = str(uuid.uuid4()) + myThingy.name
    destination = "./Remember/static/remember/images/questionImages/" + name 
    os.rename(source, destination)
    
    
    ## this is what is passed to the question for a refrence to the image.
    ## formated so it can be used directly in html
    nameForDatabase = "/../../static/remember/images/questionImages/" + name

    ## pulling data from requesting form
    
    email = request.POST['email']
    password = request.POST['password']
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']


    check = Patient.objects.filter(username = email)

    if len(check) == 0:
        ## email is not in use
        # making and saving the new patient
        newPatient = Patient(firstName=firstName, password=password, lastName=lastName, username=email, mugshot=nameForDatabase)
        newPatient.save()
        ## making a relation between patient and creater
        myNewRelation = PatientClearanceAbstraction(user=myUser, patient=newPatient, clearanceLevel = 2)
        myNewRelation.save()
        ## making base quiz for patient
        newQuiz = Quiz(patient=newPatient, order=0)
        newQuiz.save()

        return HttpResponseRedirect(reverse('Remember:pickPatient'))
    

    ## email is in use, throw error
    return render(request, 'Remember/adminEx/createPatient.html', 
    { 'error_message': "THis is dumy data",}
    ) 



## loads the set reminder page
def setReminder(request):

    return render(request, 'Remember/adminEx/setReminder.html')






## Exclusive to family
## Family Members do not get a menu, they go from selectPatient to EditQuestionnaire ##############################################
## Deleted familyMenu.html and familyEx directory
def familyMenu(request, relationID): #changed familyMainMenu to familyMenu to be consistent with previous naming convention

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    return render(request, 'Remember/familyEx/familyMenu.html', {'userRelation' : relation})







