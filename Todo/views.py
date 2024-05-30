from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login ,logout
def home(request):
   return render(request, 'Todo/home.html')
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'Todo/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user =User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentTodos')
            except IntegrityError:
                return render (request, 'Todo/signupuser.html',{'form':UserCreationForm(),'error':"username is used "})
        else:
            return render (request, 'Todo/signupuser.html',{'form':UserCreationForm(),'error':"password didnot match"})
        
        
def currentTodos(request):
    return render(request, 'Todo/currentTodos.html')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')