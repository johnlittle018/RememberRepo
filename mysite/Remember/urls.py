from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from . import views

app_name = 'Remember'
urlpatterns = [


    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),




    
    ## Stuff for everyone
    path('loginPage/', views.loginPage, name='loginPage'),
    
    path('login/', views.login, name='login'),

    path('pickPatient/', views.pickPatient, name='pickPatient'),

    path('pickedPatient/', views.pickedPatient, name='pickedPatient'),

    path('helpPage/', views.helpPage, name='helpPage'),

    path('changePassword/', views.changePassword, name='changePassword'),

    path('createAdmin/', views.createAdmin, name='createAdmin'),

   


    ## Family and Admin
    path('makeQuestion/', views.makeQuestion, name='makeQuestion'),

    path('submitQuestion/', views.submitQuestion, name='submitQuestion'),

    path('resubmitQuestion/', views.resubmitQuestion, name='resubmitQuestion'),

    path('removeQuestion/', views.removeQuestion, name='removeQuestion'),


    path('editQuestionnaire/', views.editQuestionnaire, name='editQuestionnaire'),
    path('editQuestion/', views.editQuestion, name='editQuestion'),

    ## Patient and Admin
    path('reviewResults/', views.reviewResults, name='reviewResults'),
    path('questionnaireResults/', views.questionnaireResults, name='questionnaireResults'),
    path('viewReminder/', views.viewReminder, name='viewReminder'),

   
    
    
    ## Stuff for Patient
    path('scrapbook/', views.scrapbook, name='scrapbook'), #changed Book to book
    path('takeQuestionnaire/', views.takeQuestionnaire, name='takeQuestionnaire'),
    path('takeQuestion/', views.takeQuestion, name='takeQuestion'),
    path('answerQusetion/', views.answerQusetion, name='answerQusetion'),

    path('noQuestions/', views.noQuestions, name='noQuestions'),

    path('noQuiz/', views.noQuiz, name='noQuiz'),
    

    path('patientMenu/', views.patientMenu, name='patientMenu'),


    ## Stuff for Admin 
    path('adminMenu/', views.adminMenu, name='adminMenu'),

    path('createPatient/', views.createPatient, name='createPatient'), # NEW



    path('graphsData/', views.graphsData, name='graphsData'),
    path('inviteFamily/', views.inviteFamily, name='inviteFamily'),
    path('inviteAdmin/', views.inviteAdmin, name='inviteAdmin'),
    path('processNewAdmin/', views.processNewAdmin, name='processNewAdmin'),

    path('noUser/', views.noUser, name='noUser'),
    path('newAdmin/', views.newAdmin, name='newAdmin'),

    path('submitPatient/', views.submitPatient, name='submitPatient'),

    path('newAdmin/', views.newAdmin, name='newAdmin'),

    path('managePatientPic/', views.managePatientPic, name='managePatientPic'),
    path('managePatientAccount/', views.managePatientAccount, name='managePatientAccount'),
    path('managePatientEmail/', views.managePatientEmail, name='managePatientEmail'),
    path('managePatientPassword/', views.managePatientPassword, name='managePatientPassword'),
    path('managePatientName/', views.managePatientName, name='managePatientName'),


    path('setReminder/', views.setReminder, name='setReminder'),
    #path('adminPickPatient/', views.adminPickPatient, name='adminPickPatient'), # NEW # Html file destroyed, bye bye


    ## Stuff for Family 
    path('familyMenu/', views.familyMenu, name='familyMenu'), #changed familyMainMenu to familyMenu to match previous notation



    



]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



























'''
urlpatterns = [
    path('', views.index, name='index'),
    
    
    # ex: /Remember/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /Remember/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /Remember/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
'''