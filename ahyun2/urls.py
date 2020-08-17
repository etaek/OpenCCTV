"""ahyun2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
#from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls import url

import smartcctv.views

urlpatterns = [
   path('people/',smartcctv.views.people,name='people'),
   path('register/',smartcctv.views.register, name='register'),
   path('',smartcctv.views.index, name='home'),
   path('login2/',smartcctv.views.login2,name='login2'),
   path('logout2/',smartcctv.views.logout,name='logout2'),
    path('admin/', admin.site.urls),
    path('smartcctv/', include('smartcctv.urls')),
    path('api/v1/', include('smartcctv.urls_rest')),
	path('user/add', include('smartcctv.urls_rest')),
	path('report/', smartcctv.views.report, name='report'),
	#path('register/', smartcctv.views.register, name='register'),		
    url(r'^rest-auth/', include('rest_auth.urls')),	
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
	path('index_login/', smartcctv.views.index_login, name='index_login'),	
	#path('login/', smartcctv.views.login, name='login'),
	#path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	#path('accounts/', include('django.contrib.auth.urls')),
	url(
		r'^accounts/login/',
		#auth_views.login,
		LoginView.as_view(),
		name='login',
		kwargs={
			'template_name' : 'login.html'
		}
	),
    url(
		r'^accounts/logout/',
		#auth_views.logout,
		LogoutView.as_view(),
		name='logout',
		kwargs={
			'tempate_name': 'index.html',
		}
	),
]
