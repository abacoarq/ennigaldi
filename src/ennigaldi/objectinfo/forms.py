from django import forms
from .models import ObjectIdentification

class ObjectEntry(forms.ModelForm):
    class Meta:
        model = ObjectIdentification
        fields = ('snapshot', 'hierarchy', 'work_type', 'source', 'brief_description', 'description_source', 'comments', 'distinguishing_features', 'normal_unit')

class TitleEntry(forms.ModelForm):
    class Meta:
        model = ObjectName
        fields = ('title', 'title_type', 'currency', 'level', 'note', 'source', 'lang', 'translation')
