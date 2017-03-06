from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Unit
from .forms import ParentUnitForm, ChildUnitForm, unit_formset

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
    form = ParentUnitForm
    fields = ['type', 'acronym', 'name', 'note']

    def get_context_data(self, **kwargs):
        data = super(AddUnit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['unitchildren'] = unit_formset(self.request.POST)
        else:
            data['unitchildren'] = unit_formset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        unitchildren = context['unitchildren']
        with transaction.atomic():
            self.object = form.save()

            if unitchildren.is_valid():
                unitchildren.instance = self.object
                unitchildren.save()
        return super(AddUnit, self).form_valid(form)

    def get_success_url(self):
        return reverse('unit_list')

@method_decorator(login_required, name='dispatch')
class UpdateUnit(UpdateView):
    model = Unit
    form = ParentUnitForm
    fields = ['type', 'acronym', 'name', 'parent', 'note']

    def get_context_data(self, **kwargs):
        data = super(UpdateUnit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['unitchildren'] = unit_formset(self.request.POST)
        else:
            data['unitchildren'] = unit_formset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        unitchildren = context['unitchildren']
        with transaction.atomic():
            self.object = form.save()

            if unitchildren.is_valid():
                unitchildren.instance = self.object
                unitchildren.save()
        return super(UpdateUnit, self).form_valid(form)

    def get_success_url(self):
        return reverse('unit_list')


@method_decorator(login_required, name='dispatch')
class DeleteUnit(DeleteView):
    model = Unit
    success_url = reverse_lazy('unit_list')
