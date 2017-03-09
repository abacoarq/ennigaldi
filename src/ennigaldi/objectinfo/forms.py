from django.forms import ModelForm, inlineformset_factory
from .models import ObjectIdentification, ObjectName, ObjectUnit, Dimension, TechnicalAttribute, MaterialType, Inscription

class ObjectEntry(ModelForm):
    class Meta:
        model = ObjectIdentification
        fields = ['snapshot', 'work_type', 'source', 'brief_description', 'description_source', 'comments', 'distinguishing_features', 'storage_unit', 'normal_unit']

class TitleEntry(ModelForm):
    class Meta:
        model = ObjectName
        fields = ['title', 'title_type', 'lang', 'translation', 'currency', 'level', 'note', 'source']

# Apparently the following only works with ForeignKey,
# not OneToOneField. Figure out what is the correct implementation.
preferredtitle_formset = inlineformset_factory(ObjectIdentification, ObjectName, form=ObjectEntry, extra=1)

class InscriptionEntry(ModelForm):
    class Meta:
        model = Inscription
        fields = ['inscription_display', 'inscription_position', 'inscription_type', 'inscription_language', 'inscription_notes', 'inscription_method']

# This was supposed to work. Check why it is throwing an exception.
inscription_formset = inlineformset_factory(ObjectIdentification, Inscription, form=ObjectEntry, extra=1)

###########################################################
# The following is part of Description---commented here
# just so we remember to put it where it belongs later on.

# class ColourEntry(ModelForm):
    # class Meta:
        # model = Colour
        # fields = ['colour']

# colour_formset = inlineformset_factory(ObjectIdentification, Colour, form=ObjectEntry, extra=2)

# class DimensionEntry(ModelForm):
    # class Meta:
        # model = Dimension
        # fields = ['dimension_part', 'dimension_type', 'dimension_value', 'dimension_value_qualifier']

# dimension_formset = inlineformset_factory(ObjectIdentification, Dimension, form=ObjectEntry, extra=3)

# class MaterialTypeEntry(ModelForm):
    # class Meta:
        # model = MaterialType
        # fields = ['material_type', 'material']

# materialtype_formset = inlineformset_factory(ObjectIdentification, MaterialType, form=ObjectEntry, extra=2)

# class TechnicalAttributeEntry(ModelForm):
    # class Meta:
        # model = TechnicalAttribute
        # fields = ['attribute_type', 'attribute_value']

# technicalattribute_formset = inlineformset_factory(ObjectIdentification, TechnicalAttribute, form=ObjectEntry, extra=1)


###########################################################
# The following information shall be added in separate forms,
# because it is unlikely this will be available when filling
# a field survey:
#
# - ObjectName (i.e. alternate object names)
# - OtherNumber
# - Production
# - Description > Specimen, Artifact, or WorkInstance
# - Inscription (certain fields only)
# - Rights
# - AssociatedObject
# - Ownership
# - Hierarchy (figure out a way to automatically
#   create this relationship through a button to add child
#   objects.
# - RelatedObject
# - TextRef
