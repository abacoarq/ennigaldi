from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Unit
from .forms import FieldForm

class UnitList(ListView):
    model = Unit
    paginate_by = 25
    queryset = Unit.objects.all() # default

class TopLevelUnits(ListView):
    model = Unit
    paginate_by = 25
    queryset = Unit.objects.filter(parent=None)

class UnitDetail(DetailView):
    model = Unit
    # query_pk_and_slug = True

@method_decorator(login_required, name='dispatch')
class AddUnit(CreateView):
    model = Unit
    fields = ['acronym', 'name', 'parent', 'note']

@method_decorator(login_required, name='dispatch')
class UpdateUnit(UpdateView):
    model = Unit
    fields = ['acronym', 'name', 'parent', 'note']

@method_decorator(login_required, name='dispatch')
class DeleteUnit(DeleteView):
    model = Unit
    success_url = reverse_lazy('unit_list')
