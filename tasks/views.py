from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

#Al colocar la propiedad @login_required sobre una funcion que renderiza una vista, esta va a requerir un login para acceder
#En el archivo settings.py podemos añadir una ruta en LOGIN_URL que rediriga en caso que la persona no esté logueada

def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {
            "form": UserCreationForm
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "Username already exists"
                })
        return render(request, "signup.html", {
            "form": UserCreationForm,
            "error": "Password do not match"
        })

@login_required
def tasks(request):
    # Para llamar a todas las tareas => tasks = Task.objects.all()
    
    # Para llamar a la tarea filtrada por usuario:
    # datecompleted__isnull=True son las tareas que aun no fueron realizadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    return render(request, "tasks.html", {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, "tasks.html", {'tasks': tasks})

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username of password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def create_task(request):
    if request.method == 'GET': 
        return render(request, 'create_task.html', {
        'form': TaskForm
    })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valid data'
            })

@login_required
def task_detail(request, task_id):
    #Task.objects.get(pk = task_id) funciona como un orm con la db
    # get_object_or_404 es mejor opcion, ya que si una solicitud es realizada habitualmente baja el servidor
    # Por lo tanto usandolo nos aseguramos de enviarle un error 404 al cliente de no encontrar el registro 
    if request.method == 'GET':
        task = get_object_or_404(Task, pk = task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
        'task' : task,
        'form': form
    })
    else:
        try:
            task = get_object_or_404(Task, pk = task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'error' : "Error updating task"
    })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')