from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login ,logout,authenticate
from .forms import Todoform
from .models import Todo
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
    todos = Todo.objects.all()
    return render(request, 'Todo/currentTodos.html',{'todos':todos})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'Todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'Todo/loginuser.html',{'form':AuthenticationForm(), 'error':'username and password didnot match'})
        else:
            login(request,user)
            return redirect('currentTodos')
        
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'Todo/createuser.html',{'form':Todoform()})
    else:
        try:
            form = Todoform(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currentTodos')
        except:
             return render(request, 'Todo/createuser.html',{'form':Todoform(),'error':'bad input error.'})