from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('csrf/', views.csrf),
	path('ping/', views.ping),
	path('test/<int:question_id>/', views.test),
	path('myQuery/', views.myQuery),

	#api
	path('api/v1/questions/', views.questionCollection),
	path('api/v1/questions/<int:id>/', views.questionElement),
	path('api/v1/threadtopics/', views.threadTopicCollection),
	path('api/v1/threadposts/', views.threadPostCollection),
	path('api/v1/threadposts/post/', views.postToForum),


	path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('hello/', views.HelloView.as_view(), name='hello'),
    path('forumUser/<str:email>/', views.ForumUser.as_view()),

    path('getUserSession/', views.getUserSession)
]