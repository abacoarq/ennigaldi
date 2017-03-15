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
            new_title = title_form.save()
            return HttpResponseRedirect(reverse('objectregister_form', kwargs={'objectname_id': new_title.pk}))

        else:
            return render('objectinfo/objectname_form.html', {'form': title_form})

    else:
        title_form = TitleEntry()
        return render(request, 'objectinfo/objectname_form.html', {'form': title_form})

def object_entry(request, objectname_id):
    if request.method == 'POST':
        object_form = ObjectEntry(request.POST, request.FILES, title=objectname_id)
        if object_form.is_valid():
            new_object = object_form.save()
            AccessionNumber.generate(new_object.pk)
            return HttpResponseRedirect(reverse('description_form', kwargs={'work_id': new_object.pk}))

        else:
            return render('objectinfo/objectregister_form.html', {'form': object_form}, kwargs={'objectname_id': objectname_id})

    else:
        object_form = ObjectEntry(title=objectname_id)
        return render(request, 'objectinfo/objectregister_form.html', {'form': object_form})

class DescriptionForm(CreateView):
    pass

def image_form(request):
    return HttpResponse('A form to enter images, possibly in bulk, will appear here.')

def xml(request):
    return HttpResponse('Here there be VRA Core 4 XML.')

def yaml(request):
    return HttpResponse('For a human-readable rendering in YAML of w_%s.' % work_id)
