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
from reorg.models import AccessionNumber
from .models import ObjectIdentification
from .forms import *

def index(request):
    return HttpResponse('Nothing here yet.')

@method_decorator(login_required, name='dispatch')
class AddObject(CreateView):
    model = ObjectIdentification
    form = ObjectEntry
    fields = ['snapshot', 'work_type', 'source', 'brief_description', 'description_source', 'comments', 'distinguishing_features']

    def get_context_data(self, **kwargs):
        data = super(AddObject, self).get_context_data(**kwargs)
        if self.request.POST:
            data['inscription'] = inscription_formset(self.request.POST)
        else:
            data['inscription'] = inscription_formset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        inscription = context['inscription']
        with transaction.atomic():
            self.object = form.save()
            if inscription.is_valid():
                inscription.instance = self.object
                inscription.save()

            reorg.AccessionNumber.generate(self.object.work_id)
        return super(AddObject, self).form_valid(form)

    def get_success_url(self):
        return reverse('object_list')

class ObjectList(ListView):
    model = ObjectIdentification
    paginate_by = 25
    queryset = ObjectIdentification.objects.all() # default

class ObjectDetail(DetailView):
    model = ObjectIdentification
    # query_pk_and_slug = True

def image_form(request):
    return HttpResponse('A form to enter images, possibly in bulk, will appear here.')

def xml(request):
    return HttpResponse('Here there be VRA Core 4 XML.')

def yaml(request):
    return HttpResponse('For a human-readable rendering in YAML of w_%s.' % work_id)
