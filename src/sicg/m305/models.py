from django.db import models

# Spectrum 4.0 Object Identification Information
# VRA Core 4   Namespace root level
# DCMI         Namespace root level
# SICG         1.3, 1.4, 3.4, 7.4
class ObjectId(models.Model):

    # VRA Core 4   work_id (must prepend with 'w_' when rendering).
    work_id = models.AutoField(max_length=7, primary_key=True)

    # Spectrum 4.0 Object number
    # VRA Core 4   refid
    # DCMI         identifier
    # SICG         1.4 Código identificador Iphan
    #
    # Provide a JQuery action to pre-fill this field when
    # entering a new object, to conform to the chosen
    # standard of object numbering in the organization.
    refid = models.CharField(max_length=72)

    # VRA Cores 4  work > source
    # Prepopulate with owner organization?
    source = models.CharField(max_length=200)

    # Spectrum 4.0 Brief description
    # VRA Core 4   description
    # DCMI         abstract
    # SICG         4.1 Descrição formal (compounded with other fields)
    description = models.TextField()
    description_source = models.CharField(max_length=200)

    # Spectrum 4.0 Comments
    # SICG         4.1 Descrição formal (compounded with other fields)
    comments = models.TextField()

    # Spectrum 4.0 Distinguishing features
    features = models.TextField()

    # Spectrum 4.0 Number of objects
    # DCMI         extent > count
    number_of_objects = models.PositiveIntegerField()

    # Spectrum 4.0 Object name
    # VRA Cores 4  title
    # DCMI         title
    # SICG         1.3 Identificação do bem
    object_name = models.ForeignKey(ObjectName, on_delete=models.CASCADE)

# Spectrum 4.0 Other object number
# SICG         7.4 Demais códigos
class OtherObjectNumber(models.Model):
    work = models.ForeignKey(ObjectId, on_delete=models.CASCADE)
    other_object_number = models.CharField(max_length=72)
    other_object_number_type = models.CharField(max_length=200)

class ObjectName(models.Model):
    object_name = models.CharField(max_length=200)
    # Spectrum 4.0 Object name currency
    # VRA Core 4   title_pref
    object_name_currency = models.BooleanField()
    object_name_level = models.TextField()
    object_name_note = models.TextField()
    object_name_system = models.TextField()
    # Spectrum 4.0 Object name type
    # VRA Core 4   title > type
    object_name_type = models.ForeignKey(ObjectNameType, on_delete=models.CASCADE)
    object_name_lang = models.ForeignKey(IsoLanguage, on_delete=models.CASCADE)

class ObjectNameType(models.Model):
    object_name_type = models.CharField(max_length=200)

class ObjectTitle(models.Model):
    object_title_lang = models.ForeignKey(IsoLanguage, on_delete=models.CASCADE)
    object_title = models.CharField(max_length=200)
    object_title_translation = models.CharField(max_length=200)
    object_title_type = models.ForeignKey(TitleType, on_delete=models.CASCADE)

# Spectrum 4.0 Language
# VRA Core 4   xml:lang
# DCMI         language
# Move to a specific application for metadata when project grows.
class IsoLanguage(models.Model):
    language_iso = models.CharField(max_length=16)
    language_human = models.CharField(max_length=64)
