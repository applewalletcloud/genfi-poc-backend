from django.urls import path

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
	path('api/v1/threadposts/post/', views.postToForum)
]