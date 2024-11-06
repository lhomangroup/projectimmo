from datetime import date

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import ToDoItem

class AllToDos(ListView):
    model = ToDoItem
    template_name = "todo/index.html"

class TodayToDos(ListView):
    model = ToDoItem
    template_name = "todo/today.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(due_date=date.today())