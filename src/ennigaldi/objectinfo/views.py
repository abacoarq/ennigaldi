from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from reorg.models import AccessionNumber
from .models import ObjectRegister
from .forms import *

def index(request):
    return HttpResponse('Nothing here yet.')

class ObjectList(ListView):
    model = ObjectRegister
    paginate_by = 25
    queryset = ObjectRegister.objects.all() # default

class ObjectDetail(DetailView):
    model = ObjectRegister
    # query_pk_and_slug = True


@method_decorator(login_required, name='dispatch')
class TitleEntry(CreateView):
    model = ObjectName
    form = TitleForm
    fields = ['title', 'title_type', 'lang', 'translation', 'currency', 'level', 'note', 'source']

    def get_success_url(self, **kwargs):
        return reverse('createregister_form', kwargs={ 'objectname_id' : self.object.pk})


@method_decorator(login_required, name='dispatch')
class CreateRegister(CreateView):
    model = ObjectRegister
    form = ObjectEntry
    fields = ['preferred_title', 'snapshot', 'work_type', 'source', 'brief_description', 'description_source', 'comments', 'distinguishing_features', 'normal_unit']
    pref_title = None

    def dispatch(self, request, *args, **kwargs):
        self.pref_title_id = kwargs.get('objectname_id', None)
        return super(CreateRegister, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initials = super(CreateRegister, self).get_initial()
        initials['preferred_title'] = get_object_or_404(ObjectName, pk=int(self.kwargs['objectname_id']))
        return initials

    def get_context_data(self, **kwargs):
        data = super(CreateRegister, self).get_context_data(**kwargs)
        if 'objectname_id' in self.kwargs:
            data['preferred_title'] = get_object_or_404(ObjectName, pk=self.kwargs['objectname_id'])
        if self.request.POST:
            data['inscriptions'] = inscription_formset(self.request.POST)
        else:
            data['inscriptions'] = inscription_formset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        inscription = context['inscriptions']
        with transaction.atomic():
            self.object = form.save()

            if inscription.is_valid():
                inscription.instance = self.object
                inscription.save()

            AccessionNumber.generate(self.object.work_id)
        return super(CreateRegister, self).form_valid(form)

    def get_success_url(self):
        if self.work_type == 'artifact':
            return reverse('artifact_entry', kwargs={'work_id' : self.pk})
        else:
            return reverse('object_list')


@method_decorator(login_required, name='dispatch')
class ProductionEntry(CreateView):
    model = Production
    form = ProductionForm
    fields = ['object_number', 'object_number_type']
    work_id = None

    def get_work_id(self, queryset=None):
        return queryset.get(work_id = self.work_id)

    def get_context_data(self, *args, **kwargs):
        data = super(ProductionEntry, self).get_context_data(**kwargs)
        if self.request.POST:
            data['work_id'] = work_id

class ArtifactEntry(CreateView):
    model = Artifact
    form = ArtifactForm

class WorkInstanceEntry(CreateView):
    model = WorkInstance
    form = WorkInstanceForm

def image_form(request):
    return HttpResponse('A form to enter images, possibly in bulk, will appear here.')

def xml(request):
    return HttpResponse('Here there be VRA Core 4 XML.')

def yaml(request):
    return HttpResponse('For a human-readable rendering in YAML of w_%s.' % work_id)
