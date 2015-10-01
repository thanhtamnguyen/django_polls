import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question

class QuestionMethodTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		time=timezone.now()+datetime.timedelta(days=30)
		future_question=Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)
		
	def test_was_published_recently_with_old_question(self):
		time=timezone.now()-datetime.timedelta(days=30)
		old_question=Question(pub_date=time)
		self.assertEqual(old_question.was_published_recently(), False)
		
	def test_was_published_recently_with_recent_question(self):
		time=timezone.now()-datetime.timedelta(hours=1)
		recent_question=Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), False)
		
	def create_question(t, d):
		time=timezone.now()+datetime.timedelta(days=d)
		return Question.objects.create(question_text=t,pub_date=time)



		
class QuestionViewTests(TestCase):

	def test_index_view_with_no_questions(self):
		response=self.client.get(reverse('polls:index'))
		self.assertEqual(response.statut_code,200)
		self.assertContains(response,"No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])
	
	def test_index_view_with_future_questions(self):
		create_question('Future Questions',30)
		response=self.client.get(reverse('polls:index'))
		self.assertContains(response,"No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])
		
	def test_index_view_with_past_questions(self):
		create_question('Past Questions',-30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question : Past Question>'])
	
	def test_index_view_with_future_questions_past_questions(self):
		create_question('Future Questions',-30)
		create_question('Past Questions',30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question : Past Question>'])
	
	def test_index_view_with_two_past_questions(self):
		create_question('Past Questions 1',-30)
		create_question('Past Questions 2',-5)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question : Past Question 2.>'],['<Question : Past Question 1.>'])
		
class QuestionIndexDetailTests(TestCase):

	def test_index_view_with_future_questions(self):
		create_question('Future Questions',5)
		response=self.client.get(reverse('polls:detail'),args=(future_question.id,))
		self.assertEqual(response.status_code,404)
		
	def test_index_view_with_past_questions(self):
		create_question('Past Questions',-5)
		response=self.client.get(reverse('polls:detail'),args=(past_question.id,))
		self.assertContains(response,past_question.question_text,status_code=200)	