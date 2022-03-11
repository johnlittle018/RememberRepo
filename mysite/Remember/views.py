





import email
import time
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



# importing models from our database. 
from .models import Patient, Reminder, User, PatientClearanceAbstraction, Result, Quiz, Question
# from .models import Choice, Question




### Stuff for everyone
def loginPage(request):

    return render(request, 'Remember/loginPage.html')


def login(request):

    #print(request.POST.dict())

    print("This is the login function")

    userName = request.POST['Email']
    #print(userName)

    userPassword = request.POST['password']
    #print(userPassword)

    # Checking our users
    if User.objects.filter(username = userName).exists():
        ourUser = User.objects.filter(username = userName)
        print("User is in the system.")
        if ourUser[0].password == userPassword:
            print("Password is good") 
            request.session['loggedInID'] = ourUser[0].id
            return pickPatient(request)
            #return HttpResponseRedirect(reverse('Remember:pickPatient', args=(ourUser[0].id,)))
    
    # Checking our Patients
    elif Patient.objects.filter(username = userName).exists():
        ourPatient = Patient.objects.filter(username = userName)
        print("User is in the system.")
        if ourPatient[0].password == userPassword:
            print("Password is good") 
            return HttpResponseRedirect(reverse('Remember:patientMenu'))
            
    else:
        return render(request, 'Remember/loginPage.html', {
                'error_message': "You have entered the wrong username or password, please try again",
            })


   


def pickPatient(request):

    print('This is the pick a patient view')

    currentUser = User.objects.get(pk = request.session['loggedInID'])

    usersRelations = PatientClearanceAbstraction.objects.filter(user = currentUser)

    print(usersRelations)

    #pCA is short for Patient clearance Abstraction
    return render(request, 'Remember/pickPatient.html', {'pCA' : usersRelations})


def createPatient(request):

    return render(request, 'Remember/adminEx/createPatient.html')


def helpPage(request):

    print('This is the pick a patient view')

    currentUser = User.objects.get(pk = request.session['loggedInID'])

    usersRelations = PatientClearanceAbstraction.objects.filter(user = currentUser)

    print(usersRelations)

    #pCA is short for Patient clearance Abstraction
    return render(request, 'Remember/helpPage.html')





# Function for when a patient is picked
def pickedPatient(request):

    print('This is the Picked Patient Function')

    print(request.POST.dict())


    relationID = request.POST['relation']
    #print(relationID)

    currentUser = User.objects.get(pk = request.session['loggedInID'])

    userRelation = PatientClearanceAbstraction.objects.get(pk = relationID)

    ## Cheking to see if the user realtion id we scraped from the html is
    ## a relatioinship of the user logged in through the session.
    if userRelation.user.id != currentUser.id:
        print("security is trying to be broken, send back to login page")
        return loginPage(request)

    request.session['relationshipID'] = userRelation.id

    ## this is where we check if we are relation 1 or 2 
    ## Relation 1 sends you to the family menu
    ## Relation 2 sends you to the admin menu
    if userRelation.clearanceLevel == 1:
        print("This is a family member")
        return familyMenu(request, userRelation.id)
    elif userRelation.clearanceLevel == 2:
        print("This is an admin")
        return adminMenu(request)

    else:
        print("ERRRRROOORRR!!!!!!!!")

   



    return render(request, 'Remember/newPage.html')








## family and admin

def makeQuestion(request):

    print("This is the make a question page")
    
    print(request.POST.dict())

    relationID = request.POST['relation']

    
    currentUser = PatientClearanceAbstraction.objects.get(pk = relationID)

    

    quizes = Quiz.objects.filter(patient = currentUser.patient)

    myQuize = quizes[0]

    

    return render(request, 'Remember/makeQuestion.html' , {'userRelation' : currentUser, 'quize' : myQuize})



def submitQuestion(request):

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
    
    

    myQuiz = Quiz.objects.filter(patient = relation.patient)

    print("This is the submitQuestion function")

    print(request.POST.dict())

    myImage = open('./uploads/images/images2/Bison.png')

    #myQuiz = Quiz.objects.filter(patient = 1)

    
    photoDiscription = request.POST['pDescription']
  
    question = request.POST['theQuestion']
    
    answer1 = request.POST['answer1']
 
    answer2 = request.POST['answer2']
    
    answer3 = request.POST['answer3']
 
    answer4 = request.POST['answer4']
  
    correctAnswer = request.POST.get('toggle', null)
    

    if correctAnswer == null:
        ## to do
        ## code in error that pops up, at the moment it just breaks to newPage
        print("User did not click a correct answer")
        return render(request, 'Remember/newPage.html')
    else:
        b = Question(question_text=question, description=photoDiscription, picture=myImage.name, a1=answer1, a2=answer2, a3=answer3, a4=answer4, answer=int(correctAnswer), lastSubAnswer=0, quiz=myQuiz[0] )
        #print(b.picture)
        b.save()

    return editQuestionnaire(request)


    

def resubmitQuestion(request):

    print("This is the resubmitQuestion function")

    print(request.POST.dict())

    ## temp image to use till images are figured out.
    myImage = open('./uploads/images/images2/Bison.png')

    questionID = request.POST['question']

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
    myQuestion = Question.objects.get(pk = questionID)
    
    canEdit = checkIfValidQuestionToEdit(relation, myQuestion)

    if canEdit == False: 
        return loginPage(request)



    photoDiscription = request.POST['pDescription']
  
    question = request.POST['theQuestion']
 
    answer1 = request.POST['answer1']
  
    answer2 = request.POST['answer2']
    
    answer3 = request.POST['answer3']

    answer4 = request.POST['answer4']

    correctAnswer = request.POST.get('toggle', null)
    #print(correctAnswer)

    if correctAnswer == null:
        print("User did not click a correct answer")
        #todo, code in a page refresh error for such a senario
    else:
        myQuestion.question_text = question
        myQuestion.description = photoDiscription
        myQuestion.a1 = answer1
        myQuestion.a2 = answer2
        myQuestion.a3 = answer3
        myQuestion.a4 = answer4
        myQuestion.answer = correctAnswer
        #this is where I would code in photo change if any.
        myQuestion.save()

    return editQuestionnaire(request)


def checkIfValidQuestionToEdit( relation, qestion):


    
    myQuiz = Quiz.objects.filter(patient = relation.patient)

    questions = Question.objects.filter(quiz = myQuiz[0])
    isValidQuestionToEdit = False
    for q in questions:
        if q.id == qestion.id:
            isValidQuestionToEdit = True
            break
    
    return isValidQuestionToEdit



def removeQuestion(request):


    questionID = request.POST['question']

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
    question = Question.objects.get(pk = questionID)

    isValidQuestionToEdit = checkIfValidQuestionToEdit(relation, question)


    if isValidQuestionToEdit == True:
        question.delete()
        return editQuestionnaire(request)
    else:
        return loginPage(request)








def editQuestionnaire(request):
    
    print("This is the edit questionaire page")

    print(request.POST.dict())

    
    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    print(relation.patient.name)

    myQuiz = Quiz.objects.filter(patient = relation.patient)


    myQuestions = Question.objects.filter(quiz = myQuiz[0])    

    

    return render(request, 'Remember/editQuestionnaire.html', {'userRelation' : relation, 'questions' : myQuestions})





def editQuestion(request):

    print("This is edit question")

    print(request.POST.dict())

    
    #pulling the question to be edited.
    questionID = request.POST['question']

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])
    question = Question.objects.get(pk = questionID)
    

    isValidQuestionToEdit = checkIfValidQuestionToEdit(relation, question)
            
    if isValidQuestionToEdit == True:
        return render(request, 'Remember/editQuestion.html', {'userRelation' : relation, 'question' : question})
    else:
        return loginPage(request)



    




## Patient and Admin

def reviewResults(request):

    return render(request, 'Remember/reviewResults.html')



## Stuff exclusive to patient
def scrapbook(request): #changed Book to book

    return render(request, 'Remember/patientEx/scrapbook.html')


def takeQuestionnaire(request):

    return render(request, 'Remember/patientEx/takeQuestionnaire.html')

def patientMenu(request):

    return render(request, 'Remember/patientEx/patientMenu.html')




## Exclusive to Admin

def adminMenu(request):

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    

    return render(request, 'Remember/adminEx/adminMenu.html', {'userRelation' : relation})

def graphsData(request):

    return render(request, 'Remember/adminEx/graphsData.html')

def inviteFamily(request):

    return render(request, 'Remember/adminEx/inviteFamily.html')

def inviteAdmin(request):

    return render(request, 'Remember/adminEx/inviteAdmin.html')

def setReminder(request):

    return render(request, 'Remember/adminEx/setReminder.html')

def adminPickPatient(request):

    return render(request, 'Remember/adminEx/adminPickPatient.html')


## Exclusive to family

def familyMenu(request, relationID): #changed familyMainMenu to familyMenu to be consistent with previous naming convention

    relation = PatientClearanceAbstraction.objects.get(pk = request.session['relationshipID'])

    return render(request, 'Remember/familyEx/familyMenu.html', {'userRelation' : relation})















# class IndexView(generic.ListView):
#     template_name = 'Remember/index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         return Question.objects.filter( pub_date__lte=timezone.now() ).order_by('-pub_date')[:5]

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'Remember/detail.html'
    
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte = timezone.now())


# def detail(request, question_id):

#     try:  # try allows the program to keep going with a error
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist: 
#         raise Http404("Question does not exist")
#     return render(request, 'Remember/j.html', {'question': question})











# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'Remember/results.html'


# # currently does not handle race conditions like two people voting at once, can be fixed with code from the following link. https://docs.djangoproject.com/en/3.2/ref/models/expressions/#avoiding-race-conditions-using-f
# #request.POST is a dictionary-like object that lets you access submitted data by key name. In this case, request.POST['choice'] returns the ID of the selected choice, as a string. request.POST values are always strings.
# # returns an HttpResponseRedirect rather than a normal HttpResponse. HttpResponseRedirect takes a single argument: the URL to which the user will be redirected (see the following point for how we construct the URL in this case).
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk = request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'Remember/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('Remember:results', args=(question.id,)))





