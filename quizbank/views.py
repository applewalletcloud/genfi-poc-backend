from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.middleware.csrf import get_token
from .models import Question, ThreadTopic, ThreadPost, ForumUser, ForumUserData

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer, ThreadTopicSerializer, ThreadPostSerializer, UserSerializer, SocialSerializer, ForumUserDataSerializer
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

from rest_framework.parsers import MultiPartParser, FormParser

import stripe
import json

from decimal import Decimal
from django.contrib.auth import get_user_model
from djstripe.models import Customer, Subscription

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
		print(request)
		return JsonResponse({"token": token})


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class getForumUserProfilePic(APIView):
	permission_classes = [permissions.AllowAny]
	#permission_classes = (IsAuthenticated,)
	def get(self, request, username):
		token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
		data = {'token': token}

		try: 
			userData = ForumUserData.objects.get(user_name=username)
		except ForumUserData.DoesNotExist:
			return HttpResponse(status=404)
		return FileResponse(
			open('media/' + str(userData.profile_pic), 'rb')
		)

class postForumUserProfileData(APIView):
	print("WE ENTER THE POST FORUM USER PROFILE DATA VIEW .2.2.2.22.")
	parser_classes = (MultiPartParser, FormParser)
	print("WE ENTER THE POST FORUM USER PROFILE DATA VIEW .3.3.3.3")
	def get(self, request, *args, **kwargs):
		userData = ForumUserData.objects.all()
		serializer = ForumUserDataSerializer(userData, many=True)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
		print("1111 WE ENTER THE POST FORUM USER PROFILE DATA VIEW")
		print(request)
		print("below should be the data")
		#print(request.values) #has no attribute values
		#print(request.formData)
		print(request.data)
		print(request.data["user_name"])
		print(request.data["profile_pic"])
		print("above should be the data")
		print("REQUEST DATA IS ABOVE FOR POSTING USER FORUM DATA")

		try: # if username already exists, just edit the profil pic
			print("we enter the try")
			print("we search for username " + str(request.data["user_name"]))
			user = ForumUserData.objects.get(user_name=request.data["user_name"])
			print("we found a username match in the change user profile pic view")
			user.profile_pic = request.data["profile_pic"]
			user.save()
			#user["profile_pic"].save()
			# print(" we enter the try")
			# ForumUserData.objects.update_or_create(
			# 	user_name = request.data["user_name"],
			# 	profile_pic = request.data["profile_pic"]
			# )
			# print("right about to return the ok status")
			return Response(status=status.HTTP_200_OK)
		except:
			return Response(forumUserData.errors, status=status.HTTP_400_BAD_REQUEST)
		# except: # create a new entry in the db
		# 	print("are we entering the except?")
		# 	forumUserData = ForumUserDataSerializer(data=request.data)
		# 	if forumUserData.is_valid():
		# 		forumUserData.save()
		# 		return Response(forumUserData.data, status=status.HTTP_201_CREATED)
		# 	else:
		# 		print('error', forumUserData.errors)
		# 		return Response(forumUserData.errors, status=status.HTTP_400_BAD_REQUEST)	
@api_view(('GET',))
def attachPaymentMethod(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	paymentMethodData = stripe.PaymentMethod.create(
	  type="card",
	  card={
	    "number": "4242424242424242",
	    "exp_month": 2,
	    "exp_year": 2021,
	    "cvc": "314",
	  },
	)
	user = get_user_model().objects.get(id=5)
	customer, created = Customer.get_or_create(subscriber=user.id)
	# stripe.PaymentMethod.attach(
	#   paymentMethodData.id,
	#   customer=customer.id,
	# )
	customer.add_payment_method(paymentMethodData)

	return Response(status=status.HTTP_200_OK)

@api_view(('GET',))
def testSubscription(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	user = get_user_model().objects.get(id=5)
	customer, created = Customer.get_or_create(subscriber=user.id)
	print("ARE WE MAKING IT TO THIS LINES?!")
	stripe_subscription = stripe.Subscription.create(
	  customer=customer.id,
	  items=[{"plan": "plan_GmgVUol964dCwC"}],
	)
	subscription = Subscription.sync_from_stripe_data(
		stripe_subscription
	)
	return Response(status=status.HTTP_200_OK)

from django.views.decorators.csrf import csrf_exempt



class stripePost(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self, request, *args, **kwargs):
		stripe.api_key = settings.STRIPE_SECRET_KEY # new
		print("before the charge of stripe")
		# print (request.POST)
		print(request.body) 
		body_unicode = request.body.decode('utf-8')
		body_data = json.loads(body_unicode)
		tokenData =  body_data
		print(tokenData)
		#print (request.POST["token"])
		print("request post above")
		user = get_user_model().objects.get(id=2)

		customer, created = Customer.get_or_create(subscriber=user)

		amount = Decimal(10.00)
		customer.charge(amount)
		print("do we make it past the stripe . charge . create?")
		return Response(status=status.HTTP_200_OK)

# class stripePost(APIView):
# 	permission_classes = [permissions.AllowAny]
# 	def post(self, request, *args, **kwargs):
# 		stripe.api_key = settings.STRIPE_SECRET_KEY # new
# 		print("before the charge of stripe")
# 		# print (request.POST)
# 		print(request.body) 
# 		body_unicode = request.body.decode('utf-8')
# 		body_data = json.loads(body_unicode)
# 		tokenData =  body_data
# 		print(tokenData)
# 		#print (request.POST["token"])
# 		print("request post above")
# 		charge = stripe.Charge.create(
# 			amount=500,
# 			currency='usd',
# 			description='A Django charge',
# 			source=tokenData["id"]
# 		)
# 		print("do we make it past the stripe . charge . create?")
# 		return Response(status=status.HTTP_200_OK)

		#TODO NEXT: TRY TO DO THIS WITH DJ STRIPE SINCE IT'S ATTACHED TO A CUSTOMER!
		# need to find out how subscriptions work
		# need to find out how payment types work (charge, creating charges, etc)
		# making payment vs accepting payment?



# @csrf_exempt 
# class StripeCharge():
# 	permission_classes = [permissions.AllowAny]
# 	def post(self, request):
# 		stripe.api_key = settings.STRIPE_SECRET_KEY # new
# 		print("before the charge of stripe")
# 		print (request.POST)
# 		print("request post above")
# 		charge = stripe.Charge.create(
# 			amount=500,
# 			currency='usd',
# 			description='A Django charge',
# 			source=request.POST['stripeToken']
# 		)
# 		print("do we make it past the stripe . charge . create?")
# 		return Response(status=status.HTTP_200_OK)

 # can probably delete below
class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook"""
    serializer_class = SocialSerializer
    permission_classes = [permissions.AllowAny]
 
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