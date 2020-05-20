from django.urls import path

# from rest_framework_simplejwt import views as jwt_views
from django.urls import include, path

# views
from . import views

urlpatterns = [

    # endpoint for seeing which user is associated with the jwt
    path('getUserAuthentication/', views.getUserAuthentication.as_view()),

    # endpoint for facebook social auth
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),

    # endpoint for google social auth
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),

    # endpoint for front end to get user profile pictures by username
    path('getForumUserProfilePic/<str:username>/', views.getForumUserProfilePic.as_view()),

    # endpoint for front end to change user profile picture
    path('postForumUserProfilePic/', views.postForumUserProfilePic.as_view()),
    
    # endpoint for front end to get all the main posts for all forums
    path('getForumMainPosts/', views.getForumMainPosts.as_view()),

    # endpoint for front end to get a single post by its id
    path('getForumPostByID/<int:post_id>/', views.getForumPostByID.as_view()),
    
    # endpoint for front end to get all comments needed to render a forum
    path('getForumComments/<int:main_post_id>/', views.getForumComments.as_view()),

    # endpoint for user to post comments to backend
    path('forumUserPost/', views.ForumUserPost.as_view()),
]