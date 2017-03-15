from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
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

@method_decorator(login_required, name='dispatch')
class AddObject(CreateView):
    model = ObjectRegister
    form = ObjectEntry
    fields = ['snapshot', 'work_type', 'source', 'brief_description', 'description_source', 'comments', 'distinguishing_features']

    def get_context_data(self, **kwargs):
        data = super(AddObject, self).get_context_data(**kwargs)
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

            reorg.AccessionNumber.generate(self.object.work_id)
        return super(AddObject, self).form_valid(form)

    def get_success_url(self):
        return reverse('object_list')

class ObjectList(ListView):
    model = ObjectRegister
    paginate_by = 25
    queryset = ObjectRegister.objects.all() # default

class ObjectDetail(DetailView):
    model = ObjectRegister
    # query_pk_and_slug = True

def title_entry(request):
    if request.method == 'POST':
        title_form = TitleEntry(request.POST)
        if title_form.is_valid():
            title = title_form.cleaned_data['title']
            title_type = title_form.cleaned_data['title_type']
            title_lang = title_form.cleaned_data['lang']
            title_translation = title_form.cleaned_data['translation']
            title_currency = title_form.cleaned_data['currency']
            title_level = title_form.cleaned_data['level']
            title_note = title_form.cleaned_data['note']
            title_source = title_form.cleaned_data['source']
            new_title = title_form.save()

            return HttpResponseRedirect(reverse('objectregister_form', kwargs={'objectname_id': new_title.pk}))

        else:
            return render('objectinfo/objectname_form.html', {'form': title_form})

    else:
        title_form = TitleEntry()
        return render(request, 'objectinfo/objectname_form.html', {'form': title_form})

def object_entry(request, objectname_id):
    if request.method == 'POST':
        object_form = ObjectEntry(request.POST, request.FILES)
        if object_form.is_valid():
            preferred_title = object_form.cleaned_data['preferred_title']
            snapshot = object_form.cleaned_data['snapshot']
            work_type = object_form.cleaned_data['work_type']
            source = object_form.cleaned_data['source']
            brief_description = object_form.cleaned_data['brief_description']
            description_source = object_form.cleaned_data['description_source']
            comments = object_form.cleaned_data['comments']
            distinguishing_features = object_form.cleaned_data['distinguishing_features']
            new_object = object_form.save()
            reorg.AccessionNumber.generate(new_object.pk)

            return HttpResponseRedirect(reverse(description_form, args=(new_object.pk,)))

        else:
            return render('objectinfo/objectregister_form.html', {'form': object_form})

    else:
        object_form = ObjectEntry(title=objectname_id)
        return render(request, 'objectinfo/objectregister_form.html', {'object_form': object_form})

class DescriptionForm(CreateView):
    pass

def image_form(request):
    return HttpResponse('A form to enter images, possibly in bulk, will appear here.')

def xml(request):
    return HttpResponse('Here there be VRA Core 4 XML.')

def yaml(request):
    return HttpResponse('For a human-readable rendering in YAML of w_%s.' % work_id)
