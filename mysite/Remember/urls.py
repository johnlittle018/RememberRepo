from django.urls import path

from . import views

app_name = 'Remember'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
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