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
    # Spectrum 4.0 distinguishes between name and title
    object_title = models.BooleanField()
    object_title_translation = models.CharField(max_length=200)

class ObjectNameType(models.Model):
    # to be replaced by fkey to allowed types list
    object_name_type = models.CharField(max_length=200)
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

# Spectrum 4.0 Location information
class Location(models.Model):
    None
# /Spectrum 4.0 Object location information
###########################################################

###########################################################
# Spectrum 4.0 Object description information

# Simple description fields grouped under this class
# for convenience
class ObjectDescription(models.Model):
    # Spectrum 4.0 physical description
    # VRA Core 4   description
    # DCMI         description
    physical_description = models.TextField()
    # colour to be replaced by fkey to controlled vocab
    # Spectrum 4.0 colour
    # No VRA Core 4 equivalent
    colour = CharField(max_length=64)
    # status to be replaced by fkey to list of possible statuses
    # Spectrum 4.0 status
    # VRA Core 4   status
    status = CharField(max_length=200)
    # territorial_context to be replaced by an advanced location app?
    # No Spectrum 4.0, VRA Core equivalent for territorial_context
    # SICG         1.1 Recorte territorial
    # DCMI         coverage
    territorial_context = models.CharField(max_length=200)

# Spectrum 4.0 age
# VRA Core 4   date
# DCMI         created
# SICG         2.1 Datação
# To be replaced with more robust date application that
# can be machine read to produce timelines and comparisons:
# see theoretical model at http://www.museumsandtheweb.com/biblio/issues_in_historical_geography.html
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

# object type selector should activate only
# the appropriate class, if any, below.
# VRA Core 4  StateEdition, issue
# DCMI        hasFormat, issued
class ObjectBibliographic(models.Model):
    copy_number = CharField(max_length=16)
    edition_number = CharField(max_length=64)
    form = CharField(max_length=200)

class ObjectBiological(models.Model):
    # No VRA Core 4 equivalent to BiologicalObject
    # phase to be replaced by fkey to controlled vocab
    phase = models.CharField(max_length=200)
    sex = models.BooleanField()

class ObjectArtifact(models.Model):
    # style to be replaced by fkey to controlled vocab
    # VRA Core 4  style_period
    # Dublin Core coverage
    # SICG        recorte temático
    style = models.CharField(max_length=200)
    # Cultural Context to be replaced by fkey to controlled vocab
    # No Spectrum 4.0 equivalent for Cultural Context
    # VRA Core 4   cultural_context
    # DCMI         coverage
    # SICG         1.2 Recorte temático
    cultural_context = models.CharField(max_length=200)

# Helper classes to Object Description start here.

class ObjectDescriptionContent(models.Model):
    None

class ObjectDimension(models.Model):
    None

class ObjectInscription(models.Model):
    None

class ObjectMaterial(models.Model):
    None

class TechnicalAttribute(models.Model):
    None # still have to figure out what it's supposed to do

class ObjectComponent(models.Model):
    None
# /Spectrum 4.0 Object description information
###########################################################

###########################################################
# Move to a specific application for metadata when project grows:
# Spectrum 4.0 organization, people, person
# VRA Core 4   agent
class Agent(models.Model):
    None
# /Spectrum 4.0 organization, people, person
###########################################################

###########################################################
# Move to a specific application for metadata when project grows:
# Spectrum 4.0 Language
# VRA Core 4   xml:lang
# DCMI         language
class IsoLanguage(models.Model):
    language_iso = models.CharField(max_length=16)
    language = models.CharField(max_length=64)
# /Spectrum 4.0 Language
###########################################################
