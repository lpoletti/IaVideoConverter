from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
from pytube import YouTube
import assemblyai as aai
import os
import openai

# Create your views here.
# @login_required(login_url="login")
def index(request):
    return render(request,'index.html')

def yt_title(link):
    yt = YouTube(link)
    return yt.title

def download_audio(link):
    yt = YouTube(link)
    print(yt)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base+'.mp3'
    os.rename(out_file,new_file)
    return new_file

def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = "4f9e3d78d7e84f919ab35a1afc2ff091"
    
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(audio_file)

    return transcript.text


@csrf_exempt
def generate_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': "Dado inválido enviado"},status=400)
        # get yt title
        title = yt_title(yt_link)
        # get transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error':"Falhou em transcrever"},status=500)
        # use OpenAI to generate the blog
        blog_content = generate_blog_from_transcript(transcription)
        if not blog_content:
            return JsonResponse({'error':"Falhou em gerar blog article"},status=500)

        # save blog article to database

        # return blog article as a response
        return JsonResponse({'content':blog_content})
    
    else:
        return JsonResponse({'error': 'Requisição Inválida'}, status=405)

def generate_blog_from_transcript(transcript):
    openai.api_key = 'sk-WmApiYYVy88jC01OQIvX_i-bKQu3iyYw9QDBpfcswmT3BlbkFJvt_GHW1zdULJSGNK7Oh83cBIGZd1XWUCHlvPuBMq0A'

    prompt = f'based on the following youtube video transcript, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcript}\n\nArticle:'

    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=1000
    )

    generated_content = response.choices[0].text.strip()

    return generated_content

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['senha']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            error_message = "Verifique os dados preenchidos"
            return render(request,'login.html', {error_message:error_message})

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

def user_logout(request):
    logout(request)
    return redirect('/')