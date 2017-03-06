from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from .models import Unit

class UnitList(ListView):
    model = Unit
    template_name = 'storageunit/unit_list.html' # default
    # context_object_name = unit_list # default
    paginate_by = 25
    queryset = Unit.objects.all() # default

class top_level_units(ListView):
    model = Unit
    template_name = 'storageunit/unit_list.html' # default
    paginate_by = 25
    queryset = Unit.objects.filter(parent=None)

def unit_detail(request, unit_id):
    unit_data = get_object_or_404(Unit, pk=unit_id)
    return render(request, 'storageunit/detail.html', {'unit_data': unit_data})

# @method_decorator(login_required, name='dispatch')
class FieldForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('acronym', 'name', 'parent', 'note')
