from django import template
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, response, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


from . models import Choice, Question
from polls import models

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published question"""
        return Question.objects.order_by('-pub_date')[:5]
    
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=1)
#     return render(request, 'polls/detail.html', {'question': question})

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did'nt select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return a HTTpResponseRedirect after successfully dealing
        # with POST data. This prevennts data from being posted twice if a
        # user hits the Back buttton
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))