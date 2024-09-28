from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.
# @login_required(login_url="login")
def index(request):
    return render(request,'index.html')

def user_login(request):
    return render(request,'login.html')

def user_signup(request):
    return render(request,'signup.html')