from django.forms import ModelForm, inlineformset_factory
from .models import ObjectIdentification, ObjectName, ObjectUnit, Dimension, TechnicalAttribute, MaterialType, Inscription

class ObjectEntry(ModelForm):
    class Meta:
        model = ObjectIdentification
        fields = ['snapshot', 'work_type', 'source', 'brief_description', 'description_source', 'comments', 'distinguishing_features', 'storage_unit', 'normal_unit']

# The TitleEntry form populates the preferred_title OneToOneField
# in the ObjectIdentification. It needs to be a separate form,
# not an inlineformset, as per
# http://stackoverflow.com/questions/27832076/modelform-with-onetoonefield-in-django
class TitleEntry(ModelForm):
    class Meta:
        model = ObjectName
        fields = ['title', 'title_type', 'lang', 'translation', 'currency', 'level', 'note', 'source']

class InscriptionEntry(ModelForm):
    class Meta:
        model = Inscription
        fields = ['inscription_display', 'inscription_position', 'inscription_type', 'inscription_language', 'inscription_notes', 'inscription_method']

inscription_formset = inlineformset_factory(ObjectIdentification, Inscription, form=InscriptionEntry, extra=1)

###########################################################
# The following is part of Description---commented here
# just so we remember to put it where it belongs later on.

# class ColourEntry(ModelForm):
    # class Meta:
        # model = Colour
        # fields = ['colour']

# colour_formset = inlineformset_factory(ObjectIdentification, Colour, form=ColourEntry, extra=2)

# class DimensionEntry(ModelForm):
    # class Meta:
        # model = Dimension
        # fields = ['dimension_part', 'dimension_type', 'dimension_value', 'dimension_value_qualifier']

# dimension_formset = inlineformset_factory(ObjectIdentification, Dimension, form=DimensionEntry, extra=3)

# class MaterialTypeEntry(ModelForm):
    # class Meta:
        # model = MaterialType
        # fields = ['material_type', 'material']

# materialtype_formset = inlineformset_factory(ObjectIdentification, MaterialType, form=MaterialTypeEntry, extra=2)

# class TechnicalAttributeEntry(ModelForm):
    # class Meta:
        # model = TechnicalAttribute
        # fields = ['attribute_type', 'attribute_value']

# technicalattribute_formset = inlineformset_factory(ObjectIdentification, TechnicalAttribute, form=TechnicalAttributeEntry, extra=1)


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
