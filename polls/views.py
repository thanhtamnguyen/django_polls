from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

def index(request):
	latest_question_list=Question.objects.order_by('-pub_date')[:5]
	
	# different return possible :
	
	# string concatenation from a comprehensive list
	# output=', '.join([p.question_text for p in latest_question_list])
	# return HttpResponse(output)
	
	# use template
	# template=loader.get_template('polls/index.html')
	# context=RequestContext(request, {
		# 'liste_dernieres_questions':latest_question_list,
	# })	
	# return HttpResponse(template.render(context))
	
	# without loader
	context={'liste_dernieres_questions': latest_question_list}
	return render(request, 'polls/index.html', context)

""" without view
def detail(request, question_id):
  # must check if question_id exists
	
  # with try/catch
	# try:
		# question=Question.objects.get(pk=question_id)
	# except Question.DoesNotExist:
		# raise Http404("Question does not exist")
	# return render(request, 'polls/detail.html', {'question':question})
	
	question=get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
	# version 1
	# response="You're looking at the result of question %s."
	# return HttpResponse(response %question_id)
	
	qu=get_object_or_404(Question,pk=question_id)
	return render(request, 'polls/results.html',{'question':qu})
	
def vote(request, question_id):
  # version 1
	# response="You're voting on question %s."
	# return HttpResponse(response %question_id)
	
	# v.2
	p=get_object_or_404(Question, pk=question_id)
	try:
		sel_choice=p.choice_set.get(pk=request.POST['choix'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'poll/detail.html', {
			'question':p,
			'error_message':"You didn't select a choice.",
		})
	else:
		sel_choice.votes+=1
		sel_choice.save()
		return HttpReponseRedirect(reverse('polls:results',args=(p.id,)))
"""

class IndexView(generic.ListView):
	template_name='polls/index.html'
	context_object_name='latest_question_list'
	
	def get_queryset(self):
		# return Question.objects.order_by('-pub_date')[:5]	

		return Question.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]
	
class DetailView(generic.DetailView):
	model=Question
	template_name='polls/detail.html'
	
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())
	
class ResultsView(generic.DetailView):
	model=Question
	template_name='polls/results.html'

def vote(request, question_id):
	p=get_object_or_404(Question, pk=question_id)
	try:
		sel_choice=p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question':p,
			'error_message':"You didn't select a choice.",
		})
	else:
		sel_choice.votes+=1
		sel_choice.save()
		return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))
	
	
	
