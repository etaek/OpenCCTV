
from django.shortcuts import render,redirect
from django.http import HttpResponse
#from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.core import serializers
from .models import PeopleCount
import json
# Create your views here.

def index(request):
	
    return render(request, 'pages/index.html', {})

#def post_create(request):
    
 #   form=PostForm(request.POST)
 #   if form.is_valid():
 #       form.save()
    
 #   return render(request,'pages/login.html',{'form':form})

# 로그인
def login2(request):
	if request.method == "POST":
		username=request.POST.get("username")
		password=request.POST.get("password")
		print(username)
		print(password)
		user=authenticate(username=username, password=password)
		if user:
			print("인증성공")
			login(request,user)
			return render(request, 'pages/index_login.html')
		else:
			print("인증실패")
	return render(request, 'registration/login.html')

def logout(request):
	auth.logout(request)
	return redirect('home')

def report(request):
#	json_data=serializers.serialize("json",PeopleCount.objects.all())
#	people=PeopleCount.objects.all()
	people=PeopleCount.objects.filter(date__contains='2020')
#	people=list(people.values())
	#context_dict['people_list']=json.dumps(people)
	#for peo in people:
	#	print(peo.date)
	
	return render(request, 'pages/report.html',{'people_list':people})

def index_login(request):
	return render(request, 'pages/index_login.html')

#def register(request):
#	if request.method == "GET":
#		return render(request, 'pages/register.html')
#	elif request.method == "POST":
#		name = request.POST['name']
#		email = request.POST['email']
#		password = request.POST['inputPassword']
#		re_password = request.POST['inputConfirmPassword']
#
#		model = smartcctv(
#			name = name,
#			password = password,
#		)
#		model.save()
#
#		return render(request, 'pages/register.html')


# 회원가입
def register(request):
	if request.method=='POST':
		if request.POST.get("inputPassword")==request.POST.get("inputConfirmPassword"):
			user=User.objects.create_user(
			username=request.POST.get("username"),email=request.POST.get("email"),
			password=request.POST.get("inputPassword"))
			user.last_name=request.POST.get("lastname")
			user.first_name=request.POST.get("firstname")
			user.save()
			#auth.login(request,user)
			return redirect('home')
		return render(request,'register.html')
	return render(request,'register.html')

def people(request):
	template_name='pages/examples.html'
	people_num=PeopleCount.objects.all()
	return render(request, template_name, {'people_num':people_num})


