from django.db import models

###########################################################
# Spectrum 4.0 Object Identification Information
# VRA Core 4   Namespace root level
# DCMI         Namespace root level
# SICG         1.3, 1.4, 3.4, 7.4
class ObjectId(models.Model):
    # VRA Core 4   work_id
    # Must prepend with 'w_' when rendering XML.
    work_id = models.AutoField(max_length=7, primary_key=True)
    # Spectrum 4.0 Object number
    # VRA Core 4   refid
    # DCMI         identifier
    # SICG         1.4 Código identificador Iphan
    # Provide a JQuery action to pre-fill this field when
    # entering a new object, to conform to the chosen
    # standard of object numbering in the organization.
    # Also make up another application to keep track of the
    # object numbers.
    refid = models.CharField(max_length=72)
    # VRA Core 4   work > source
    # Auto populate with owner organization?
    # Turn this into a fk for an agent model.
    source = models.CharField(max_length=200)
    # Spectrum 4.0 Brief description
    # VRA Core 4   description
    # DCMI         abstract
    # SICG         4.1 Descrição formal (compounded with other fields)
    description = models.TextField()
    # Turn this into a fk for a bibliography model.
    description_source = models.CharField(max_length=200)
    # Spectrum 4.0 Comments
    # SICG         4.1 Descrição formal (compounded with other fields)
    comments = models.TextField()
    # Spectrum 4.0 Distinguishing features
    distinguishing_features = models.TextField()
    # Spectrum 4.0 Number of objects
    # DCMI         extent > count
    # SICG         3.4.2.1 Número de partes
    number_of_objects = models.PositiveIntegerField()
    # SICG         1.1 Recorte territorial
    territorial_context = models.CharField(max_length=200)
    # VRA Core 4   cultural_context
    # DCMI         coverage
    # SICG         1.2 Recorte temático
    cultural_context = models.CharField(max_length=200)

# Spectrum 4.0 Other object number
# SICG         7.4 Demais códigos
class OtherObjectNumber(models.Model):
    work = models.ForeignKey(ObjectId, on_delete=models.CASCADE)
    other_object_number = models.CharField(max_length=72)
    other_object_number_type = models.CharField(max_length=200)

# Spectrum 4.0 Object name
# VRA Core 4   title
# DCMI         title
# SICG         1.3 Identificação do bem
class ObjectName(models.Model):
    work = models.ForeignKey(ObjectId, on_delete=models.CASCADE)
    object_name = models.CharField(max_length=200)
    # Spectrum 4.0 Object name currency
    # VRA Core 4   title
    object_name_currency = models.BooleanField()
    object_name_level = models.TextField()
    # Spectrum 4.0 Object name notes
    # VRA Core 4   title > source
    object_name_note = models.TextField()
    object_name_system = models.CharField(max_length=72)
    object_name_lang = models.ForeignKey(IsoLanguage, on_delete=models.CASCADE)
    # Spectrum 4.0 Object name type
    # VRA Core 4   title > type
    object_name_type = models.ForeignKey(ObjectNameType, on_delete=models.CASCADE)
    # VRA Core 4   title > pref
    # DCMI         title.alternative
    object_name_preferred = models.BooleanField()

class ObjectNameType(models.Model):
    object_name_type = models.CharField(max_length=200)

# Spectrum 4.0 Object title
# VRA Core 4   title
# DCMI         title
class ObjectTitle(models.Model):
    work = models.ForeignKey(ObjectId, on_delete=models.CASCADE)
    object_title = models.CharField(max_length=200)
    object_title_translation = models.CharField(max_length=200)
    object_title_language = models.ForeignKey(IsoLanguage, on_delete=models.CASCADE)
    object_title_type = models.ForeignKey(ObjectNameType, on_delete=models.CASCADE)
    # VRA Core 4   title > pref
    # DCMI         title.alternative
    object_title_preferred = models.BooleanField()

# /Spectrum 4.0 Object identification information
###########################################################

###########################################################
# Spectrum 4.0 Object production information
# VRA Core 4   date, agent
# DCMI         created
class ObjectProduction(models.Model):
    work = models.ForeignKey(ObjectId, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delet=models.SET_NULL)
    production_note = models.TextField()
    # Move this to a Foreign key later on
    production_location = models.CharField(max_length=200)
    # Spectrum 4.0 Technique
    # VRA Core 4   tech_name
    production_technique = models.CharField(max_length=200)
    production_technique_type = models.ForeignKey(TechniqueType, on_delete=models.PROTECT)
# /Spectrum 4.0 Object production information
###########################################################

###########################################################
# Spectrum 4.0 Object location information
class ObjectLocation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    location_fitness = models.textField()
    location_note = models.textField()
    location_date = models.DateField()
    normal_location = models.ForeignKey(Location, on_delete=models.PROTECT)
# /Spectrum 4.0 Object location information
###########################################################

###########################################################
# Spectrum 4.0 Object description information, production date
# To be replaced with more robust date application that
# can be machine read to produce timelines and comparisons:
# see theoretical model at http://www.museumsandtheweb.com/biblio/issues_in_historical_geography.html
# VRA Core 4   date
# DCMI         created
# SICG         2.1 Datação
class ObjectDate(models.Model):
    date_type = models.ForeignKey(DateType, on_delete=models.PROTECT)
    date_earliest = models.CharField(max_length=200)
    date_earliest_accuracy = models.ForeignKey(DateAccuracy, on_delete=models.PROTECT)
    date_earliest_unit = models.ForeignKey(AgeUnit, on_delete=models.PROTECT)
    date_latest = models.CharField(max_length=200)
    date_latest_accuracy = models.ForeignKey(DateAccuracy, on_delete=models.PROTECT)
    date_latest_unit = models.ForeignKey(AgeUnit, on_delete=models.PROTECT)
    date_source = models.CharField(max_length=200)

# Spectrum 4.0 Age qualification
# VRA Core 4   date_type
class DateType(models.Model):
    date_type = models.CharField(max_length=72)

# VRA Core 4   date_earliest_accuracy, date_latest_accuracy
class DateAccuracy(models.Model):
    date_accuracy = models.CharField(max_length=200)

# Spectrum 4.0 Age unit
class AgeUnit(models.Model):
    age_unit = models.CharField(max_length=72)

# Spectrum 4.0 Production > Technique type
class TechniqueType(models.Model):
    production_technique_type = models.CharField(max_length = 200)

# Move to a specific application for metadata when project grows:
# Spectrum 4.0 organization, people, person
# VRA Core 4   agent
class Agent(models.Model):
    None

# Move to a specific application for metadata when project grows:
# Spectrum 4.0 Language
# VRA Core 4   xml:lang
# DCMI         language
class IsoLanguage(models.Model):
    language_iso = models.CharField(max_length=16)
    language = models.CharField(max_length=64)

###########################################################
# Spectrum 4.0 Location information
class Location(models.Model):
    None
# /Spectrum 4.0 Location information
###########################################################
