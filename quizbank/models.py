import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)

	def __str__(self):
		return self.choice_text

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer_text = models.CharField(max_length=200)

	def __str__(self):
		return self.answer_text

class ThreadTopic(models.Model):
	topic_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	last_update = models.DateTimeField('last updated', default=timezone.now())
	summary_text = models.CharField(max_length=200, default="this is a default summary")
	num_comments = models.IntegerField(default=0)

	def __str__(self):
		return self.topic_text

class ThreadPost(models.Model):
	thread_topic = models.ForeignKey(ThreadTopic, on_delete=models.CASCADE)
	thread_text = models.CharField(max_length=200)
	thread_creator = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')


	def __str_(self):
		return self.thread