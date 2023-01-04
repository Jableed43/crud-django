from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    # Generamos la relacion entre la tarea y el modelo de usuario
    # El metodo on_delete.Cascade al ser eliminado el usuario tambien lo son sus tareas por cascada
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #Permite visualizar titulo y nombre del usuario creador de la tarea en el listado de Tasks
    def __str__(self):
        return self.title + '- by ' + self.user.username