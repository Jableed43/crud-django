from .models import Task
from django import forms

#Creamos nuestro propio form, importamos el modelo task
#Decidimos cuales de los campos de este modelo precisamos en el form web
#Para poder modificar el formulario de las tareas, es necesario crear un widget, que es un diccionario
#Con este diccionario podemos pasarle a un objeto los inputs y sus atributos
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        #diccionario
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto mb-3'})

        }
