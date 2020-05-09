from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from .models import Question, ThreadTopic, ThreadPost, ForumUser

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer, ThreadTopicSerializer, ThreadPostSerializer, UserSerializer, SocialSerializer
from rest_framework.parsers import JSONParser
from django.utils import timezone


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, permissions, status, views
from requests.exceptions import HTTPError
 
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, BasePermission


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


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

@api_view(['GET'])
def threadTopicCollection(request):
	if request.method == 'GET':
		threadTopics = ThreadTopic.objects.all()
		serializer = ThreadTopicSerializer(threadTopics, many=True)
		return Response(serializer.data)

@api_view(['GET'])
def threadPostCollection(request):
	if request.method == 'GET':
		threadPosts = ThreadPost.objects.all()
		serializer = ThreadPostSerializer(threadPosts, many=True)
		return Response(serializer.data)

@api_view(['POST'])
def postToForum(request):
	data = JSONParser().parse(request)
	threadTopics = ThreadTopic.objects.all()
	newPost = ThreadPost(thread_topic=threadTopics[int(data['id'])], thread_text=data['text'], thread_creator="roboman", pub_date=timezone.now())
	serializer = ThreadPostSerializer(newPost)

	try:
		newPost.save()
	except:
		return Response({"success": True}, status=400)
	return Response({"success": False}, status=201)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

# i think this is no longer in use. can probably delete
class ForumUser(APIView):
	def get(self, request, email):
		print("we are printing the formuser api stuff")
		print(email)
		#user = User.objects.get(email=email)
		users = User.objects.all()
		user = "user not found"
		serializer = None
		for curr in users:
			if email == curr.email:
				serializer = UserSerializer(curr)
		print(user)
		if not serializer:
			# make the user here...
			# then return it!

			return Response({"user": user})
		else:
			return Response({"user": serializer.data})

	def post(self, request):
		data = JSONParser.parse(request)
		newForumUser = ForumUser()
		newUser = User()
		try:
			newForumUser.save()
			newUser.save()
		except: # i think this is the wrong order and except is in the failure case?
			return Response({"success": True}, status=400)
		return Response({"success": False}, status=201)

@csrf_exempt

def getUserSession(request):
    current_user = request.user
    print("user info below!!!")
    print(current_user)
    print (current_user.id)
    session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
    print("session key below")
    print (session_key)
    print("request session below")
    print(request.session.session_key)
    print('is the user authenticated?')
    print(current_user.is_authenticated)
    return JsonResponse({"token": request.session.session_key})

# api endpoint where the client gives a JWT and gets the user associated with the JWT
class getUserAuthentication(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		print(request)
		print("ARE WE CALLING GETUSERAUTHENTICATION?")
		print(request.user)
		token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
		print(token)
		data = {'token': token}
		print("the request is below")
		print(request.user)
		return JsonResponse({"user": str(request.user), "token": token})


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
 
class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook"""
    serializer_class = SocialSerializer
    permission_classes = [permissions.AllowAny]
 
    def get(self, request):
        console.log(request.data)

    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)
 
        try:
            backend = load_backend(strategy=strategy, name=provider,
            redirect_uri=None)
 
        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'},
            status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)
        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            authenticated_user = backend.do_auth(access_token, user=user)
       
        except HTTPError as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
       
        except AuthForbidden as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
 
        if authenticated_user and authenticated_user.is_active:
            #generate JWT token
            #login(request, authenticated_user)
            print("DO YOU SEE ME PRINTING HERE?!")
            print(authenticated_user)
            data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )}
            #customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                "token": data.get('token')
            }
            return Response(status=status.HTTP_200_OK, data=response)