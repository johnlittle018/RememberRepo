





from django.http import Http404
from django.http import HttpResponse
from django.utils import timezone
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.views import generic
from django.urls import reverse
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'Remember/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter( pub_date__lte=timezone.now() ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'Remember/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte = timezone.now())


def detail(request, question_id):

    try:  # try allows the program to keep going with a error
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist: 
        raise Http404("Question does not exist")
    return render(request, 'Remember/j.html', {'question': question})





## new stuff for Remember




### Stuff for everyone
def loginPage(request):

    return render(request, 'Remember/newPage.html')


## Stuff exclusive to patient
def scrapBook(request):

    return render(request, 'Remember/newPage.html')


def takeQuestionnaire(request):

    return render(request, 'Remember/newPage.html')

def patientMenu(request):

    return render(request, 'Remember/newPage.html')


def reviewResults(request):

    return render(request, 'Remember/newPage.html')




























class ResultsView(generic.DetailView):
    model = Question
    template_name = 'Remember/results.html'


# currently does not handle race conditions like two people voting at once, can be fixed with code from the following link. https://docs.djangoproject.com/en/3.2/ref/models/expressions/#avoiding-race-conditions-using-f
#request.POST is a dictionary-like object that lets you access submitted data by key name. In this case, request.POST['choice'] returns the ID of the selected choice, as a string. request.POST values are always strings.
# returns an HttpResponseRedirect rather than a normal HttpResponse. HttpResponseRedirect takes a single argument: the URL to which the user will be redirected (see the following point for how we construct the URL in this case).
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'Remember/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('Remember:results', args=(question.id,)))





