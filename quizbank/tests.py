import datetime

from django.test import TestCase
from django.utils import timezone
from django.test import Client

# allows us to search for urls by their name
from django.urls import reverse

from .models import Question
# Create your tests here.

# instantiate client
client = Client()

class QuizbankTests(TestCase):
	# this test is to see if our tests work properly
	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)


def create_question(question_text, days):
	# create question with the given question_text , along with a days (a timedelta) relative to now
	time = timezone.now() + datetime.timedelta(day = days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
	# test made to practice  using a client in django tests
	def test_index_endpoint(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Hello, this is the quizbank index!")