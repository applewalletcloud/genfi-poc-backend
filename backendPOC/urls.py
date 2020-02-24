"""backendPOC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token

#from django.conf.urls import include
urlpatterns = [
    path('quizbank/', include('quizbank.urls')),
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('api/auth/oauth/', include('rest_framework_social_oauth2.urls')), # note this is the same as the above line!
    path('api-token-auth/', obtain_jwt_token),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    #path('login/', auth_views.login, name="login"),
    #path('logout/', auth_views.logout, name="logout"),
    #path('oauth/', include('social_django.urls', namespace='social')),
]
