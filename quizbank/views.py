from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from .models import Question 

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer


# Create your views here.
def index(request):
	return HttpResponse("Hello, this is the quizbank index!")

def csrf(request):
	return JsonResponse({'csrfToken': get_token(request)})

def ping(request):
	return JsonResponse({'result': 'We are doing okay!'})

def getQuestion(request):
	return JsonResponse({'question': 'need to keep coding the views page'})

def test(request, question_id):
	return HttpResponse(question_id);

def myQuery(request):
	random_question = Question.objects.all()[0];
	output = random_question.question_text;
	return JsonResponse({'question': output});

@api_view(['GET'])
def questionCollection(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def questionElement(request, id):
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)