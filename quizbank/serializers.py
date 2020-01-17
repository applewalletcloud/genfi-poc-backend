from rest_framework import serializers
from .models import Question
from .models import ThreadTopic
from .models import ThreadPost

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'pub_date')

class ThreadTopicSerializer(serializers.ModelSerializer):
	class Meta:
		model = ThreadTopic
		fields = ('id', 'topic_text', 'pub_date', 'last_update', 'summary_text', 'num_comments', 'creator')

class ThreadPostSerializer(serializers.ModelSerializer):
	class Meta:
		model = ThreadPost
		fields = '__all__'