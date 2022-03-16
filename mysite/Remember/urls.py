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

   


        

    ## Family and admin
    path('makeQuestion/', views.makeQuestion, name='makeQuestion'),

    path('submitQuestion/', views.submitQuestion, name='submitQuestion'),

    path('resubmitQuestion/', views.resubmitQuestion, name='resubmitQuestion'),

    path('removeQuestion/', views.removeQuestion, name='removeQuestion'),


    path('editQuestionnaire/', views.editQuestionnaire, name='editQuestionnaire'),
    path('editQuestion/', views.editQuestion, name='editQuestion'),

    ## Patient and Admin
    path('reviewResults/', views.reviewResults, name='reviewResults'),
    
    
    ## Stuff for Patient
    path('scrapbook/', views.scrapbook, name='scrapbook'), #changed Book to book
    path('takeQuestionnaire/', views.takeQuestionnaire, name='takeQuestionnaire'),
    path('patientMenu/', views.patientMenu, name='patientMenu'),
    path('viewReminder/', views.viewReminder, name='viewReminder'),


    ## Stuff for Admin 
    path('adminMenu/', views.adminMenu, name='adminMenu'),





    path('graphsData/', views.graphsData, name='graphsData'),
    path('inviteFamily/', views.inviteFamily, name='inviteFamily'),
    path('inviteAdmin/', views.inviteAdmin, name='inviteAdmin'),
    path('setReminder/', views.setReminder, name='setReminder'),
    path('adminPickPatient/', views.adminPickPatient, name='adminPickPatient'), # NEW


    ## Stuff for Family 
    path('familyMenu/', views.familyMenu, name='familyMenu'), #changed familyMainMenu to familyMenu to match previous notation



    



]






























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