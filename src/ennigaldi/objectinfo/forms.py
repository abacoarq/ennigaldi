from django import forms
from .models import ObjectIdentification

class ObjectEntry(forms.ModelForm):

    class Meta:
        model = ObjectIdentification
        fields = ('work_snapshot', 'preferred_title')
