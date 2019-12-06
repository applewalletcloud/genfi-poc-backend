from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token

# Create your views here.
def index(request):
	return HttpResponse("Hello, this is the quizbank index!")

def csrf(request):
	return JsonResponse({'csrfToken': get_token(request)})

def ping(request):
	return JsonResponse({'result': 'We are doing okay!'})

def getQuestion(request):
	return JsonResponse({'question': 'need to keep coding the views page'})