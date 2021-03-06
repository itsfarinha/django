from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.utils import timezone

# Create your views here.

# generic views way


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # list view also uses a default template, so it's necessary to set the template name here too
    context_object_name = 'latest_question_list'
    # in this case, was necessary to tell django the name of the context variable because the automatically generated
    # context variable is 'question_list', so instead of change this variable in the template, it's easier to
    # specify here using 'context_object_name'.

    """def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]"""
    #  the method above returns all the questions, including those set to be published in the future
    #  This new method returns only the last five questions
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    # tell django to use an specific template instead of the autogenerated default template.
    # <app name/<model name>_detail.html --> default template

    # The variable 'question' used in the functions views is automatically provided in detail views, django knows
    # to generate an appropriate name for the context variable.

    def get_queryset(self):

        """
        Excludes any questions that aren't published yet
        """

        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    # both results and detail view should return the same appearance
    # template when rendered, but the specific template_name ensures
    # the difference between them.


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question,
                                                     'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
        # always return a redirect after a post


# same views but in function views way
"""def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # 1
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist!')
    return render(request, 'polls/detail.html', {'question': question})
    # 2
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/results.html', {'question': question})"""