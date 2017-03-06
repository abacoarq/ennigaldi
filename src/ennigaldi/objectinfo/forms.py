from django import forms
from .models import ObjectIdentification

class ObjectEntry(forms.ModelForm):

    class Meta:
        model = ObjectIdentification
        fields = ('snapshot', 'preferred_title', 'hierarchy', 'work_type', 'source', 'brief_description', 'description_source', 'comments', 'distinguishing_features', 'production', 'storage_unit', 'normal_unit')
