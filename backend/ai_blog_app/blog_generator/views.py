from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
# @login_required(login_url="login")
def index(request):
    return render(request,'index.html')

def user_login(request):
    return render(request,'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email= request.POST['email']
        password = request.POST['senha']
        repeatPass = request.POST['repeatSenha']
        if password == repeatPass:
            try:
                user = User.objects.create_user(username,email,password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Erro ao criar o usuário'
                return render(request,'signup.html', {error_messsage:error_message})

        else:
            error_message = "Senhas não são iguais"
            return render(request,'signup.html', {error_messsage:error_message})
    return render(request,'signup.html')