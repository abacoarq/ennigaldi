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


# The TitleForm must be filled first so that its pk can be used in
# the ObjectEntry form.
@method_decorator(login_required, name='dispatch')
class TitleEntry(CreateView):
    model = ObjectName
    form = TitleForm
    fields = ['title', 'title_type', 'lang', 'translation', 'currency', 'level', 'note', 'source']

    def get_success_url(self, **kwargs):
        return reverse('createregister_form', kwargs={ 'objectname_id' : self.object.pk})


# The ObjectEntry form needs to be loaded after the TitleForm has been saved.
@method_decorator(login_required, name='dispatch')
class CreateRegister(CreateView):
    model = ObjectRegister
    form = ObjectEntry
    fields = ['preferred_title', 'snapshot', 'work_type', 'source', 'brief_description', 'description_source', 'comments', 'distinguishing_features', 'normal_unit']

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
            data['dimensions'] = dimension_formset(self.request.POST)
            data['other_numbers'] = number_formset(self.request.POST)
        else:
            data['inscriptions'] = inscription_formset()
            data['dimensions'] = dimension_formset()
            data['other_numbers'] = number_formset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        inscription = context['inscriptions']
        dimension = context['dimensions']
        other_number = context['other_numbers']
        with transaction.atomic():
            self.object = form.save()

            AccessionNumber.generate(self.object.work_id)

            if inscription.is_valid():
                inscription.instance = self.object
                inscription.save()

            if dimension.is_valid():
                dimension.instance = self.object
                dimension.save()

            if other_number.is_valid():
                other_number.instance = self.object
                other_number.save()

        return super(CreateRegister, self).form_valid(form)

    def get_success_url(self):
        return reverse('object_list')
        # In a field survey it does not make sense to fill out
        # an exhaustive set of data before proceeding to the next
        # object. Figure out some sort of selector to change this
        # when registering the objects with complete information
        # is desirable.
        # if self.work_type == 'specimen':
            # return reverse('specimen_entry', kwargs={'work_id' : self.pk})
        # elif self.work_type == 'workInstance':
            # return reverse('instance_entry', kwargs={'work_id' : self.pk})
        # else:
            # return reverse('artifact_entry', kwargs={'work_id' : self.pk})


@method_decorator(login_required, name='dispatch')
class DescriptionEntry(CreateView):
    # def form_valid(self, form):
        # context = self.get_context_data()
        # dimension = context['dimension']
        # with transaction.atomic():
            # self.object = form.save()

            # if dimension.is_valid():
                # dimension.instance = self.object()
                # dimension.save()

        # return super(DescriptionEntry, self).form_valid(form)

    def get_success_url(self):
        return reverse('object_list')

    class Meta:
        abstract = True


@method_decorator(login_required, name='dispatch')
class SpecimenEntry(DescriptionEntry):
    model = Specimen
    form = SpecimenForm
    fields = ['physical_description', 'colour', 'description_display', 'specimen_age', 'specimen_age_qualification', 'specimen_age_unit', 'phase', 'sex', 'object_date']


@method_decorator(login_required, name='dispatch')
class ArtifactEntry(DescriptionEntry):
    model = Artifact
    form = ArtifactForm
    fields = ['physical_description', 'colour', 'technical_attribute', 'description_display']

    def get_success_url(self):
        return reverse('production_entry', kwargs={'work_id' : self.pk})


@method_decorator(login_required, name='dispatch')
class InstanceEntry(ArtifactEntry):
    model = WorkInstance
    form = InstanceForm


@method_decorator(login_required, name='dispatch')
class ProductionEntry(CreateView):
    model = Production
    form = ProductionForm
    fields = []

    def get_work(self):
        work = get_object_or_404(ObjectRegister, pk=int(self.kwargs['work_id']))
        return work

    def get_context_data(self, *args, **kwargs):
        data = super(ProductionEntry, self).get_context_data(**kwargs)
        if self.request.POST:
            data['work_id'] = work_id


def image_form(request):
    return HttpResponse('A form to enter images, possibly in bulk, will appear here.')

def xml(request):
    return HttpResponse('Here there be VRA Core 4 XML.')

def yaml(request):
    return HttpResponse('For a human-readable rendering in YAML of w_%s.' % work_id)
