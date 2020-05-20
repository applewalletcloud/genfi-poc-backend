# rest framework api
from rest_framework.views import APIView
from rest_framework import generics, permissions, status, views

# models
from .models import ForumUserProfilePic, ForumPost

# serializers/parsers
from .serializers import ForumPostSerializer
from rest_framework.parsers import JSONParser

# responses
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse, FileResponse
 
# permission classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated

# imported for social login
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

# timezone
from django.utils import timezone


# Create your views here.

# api endpoint where the client gives a JWT and gets the user associated with the JWT
class getUserAuthentication(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
		data = {'token': token}
		return JsonResponse({"user": str(request.user), "token": token})

# required view for google social auth
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

# required view for facebook social auth
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

'''
view for getting the user's profile picture
if the user has never set a profile picture before, then a default picture of gon is used
'''
class getForumUserProfilePic(APIView):
    permission_classes = [permissions.AllowAny]
    #permission_classes = (IsAuthenticated,)
    def get(self, request, username):
        # checks to see if the user already has a profile pic
        try: 
            userData = ForumUserProfilePic.objects.get(user_name=username)
        except ForumUserProfilePic.DoesNotExist:
            # here we want to create an entry with our default profile pic and return it
            newEntry = ForumUserProfilePic(user_name=username, profile_pic = 'media/images/default.png')
            newEntry.save()
            return FileResponse(
                open('media/images/default.png', 'rb')
            )
        return FileResponse(
            open(str(userData.profile_pic), 'rb')
        )

'''
endpoint for users to change their forum profile picture
'''
class postForumUserProfilePic(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        # if username already exists, just edit the profile pic
        try: 
            # get the current user profile pic entry
            user = ForumUserProfilePic.objects.get(user_name=request.data["user_name"])
            # replace the profile pic data
            user.profile_pic = request.data["profile_pic"]
            # save the entry with the new profile pic data
            user.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(forumUserData.errors, status=status.HTTP_400_BAD_REQUEST)


'''
endpoint for getting the main posts of all forums
used to display the home page for the front end
'''
class getForumMainPosts(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        posts = ForumPost.objects.filter(is_main_post=True)
        serializer = ForumPostSerializer(posts, many=True)
        return Response(serializer.data)

'''
Endpoint for front end to get a single forum post by its id
'''
class getForumPostByID(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, post_id, *args, **kwargs):
        post = ForumPost.objects.get(post_id=post_id)
        serializer = ForumPostSerializer(post)
        return Response(serializer.data)

'''
Endpoint for front end to query forum comments to display
'''
class getForumComments(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, main_post_id, *args, **kwargs):
        posts = ForumPost.objects.filter(is_main_post=False, main_post_id=main_post_id)
        serializer = ForumPostSerializer(posts, many=True)
        return Response(serializer.data)

'''
Endpoint for forum users to post to a forum
'''
class ForumUserPost(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = JSONParser().parse(request)
        ForumPost.objects.all()
        # get all the details for what we want to post
        # make a new post
        newForumPost = ForumPost(
            is_main_post = data["is_main_post"],
            post_id = ForumPost.objects.count()+1,
            main_post_id = data["main_post_id"],
            parent_id = data["parent_id"],
            creator = data["creator"],
            post_title = data["post_title"],
            post_text = data["post_text"],
            indentation_level = data["indentation_level"]
            )
        serializer = ForumPostSerializer(newForumPost)
        try:
            newForumPost.save()
        except:
            return Response({"success": True}, status=400)
        return Response({"success": False}, status=201)
        
        