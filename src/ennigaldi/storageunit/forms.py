from django.forms import ModelForm
from django.forms import inlineformset_factory
from .models import Unit

class ParentUnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['acronym', 'name', 'note']

class ChildUnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['acronym', 'name', 'note']

unit_formset = inlineformset_factory(Unit, Unit, form=ParentUnitForm, extra=3)
