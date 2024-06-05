from urllib import request
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import redirect, render,get_object_or_404
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
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)    
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
         
         
def viewtodo(request, todo_pk):
    todo = Todo.objects.get(pk=todo_pk, user = request.user)
    if request.method == 'GET':
        form = Todoform(instance=todo)
        return render(request, 'Todo/viewtodo.html',{'todo':todo, 'form':form})
    else:
        try:
            form = Todoform(request.POST, instance=todo)
            form.save()
            return redirect('currentTodos')
        except:
            return render(request, 'Todo/viewtodo.html',{'todo':todo, 'form':form, 'error':'bad input error.'})
    
    
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currentTodos')


def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currentTodos')