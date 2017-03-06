from django.forms import ModelForm
from .models import Unit

class FieldForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['acronym', 'name', 'parent', 'note']
