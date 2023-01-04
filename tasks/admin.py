from django.contrib import admin
from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    #Created lleva coma ya que es una tupla
    readonly_fields = ('created',)

admin.site.register(Task, TaskAdmin)