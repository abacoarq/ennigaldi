from django.db import models

###########################################################
# Spectrum 4.0 Object Identification Information
# VRA Core 4   Namespace root level
# DCMI         Namespace root level
# SICG         1.3, 1.4, 3.4, 7.4
class ObjectIdentification(models.Model):
    # VRA Core 4   work_id, must prepend with 'w_' when rendering XML.
    # DCMI         identifier
    # This is NOT the object accession number but a unique identifier!
    # (See the VRA Core 4 spec for clarification)
    work_id = models.AutoField(max_length=7, primary_key=True)
    # Spectrum 4.0 Object number
    # VRA Core 4   refid
    # SICG         1.4 Código identificador Iphan
    # This IS the object accession number used in the organization.
    # Provide a JQuery action to pre-fill this field when
    # entering a new object, to conform to the chosen
    # standard of object numbering in the organization.
    # Also make up another application to keep track of the
    # object numbers.
    refid = models.CharField(max_length=72)
    # VRA Core 4   work > source
    # Auto populate with owner organization?
    # Turn this into a fk for an agent model?
    source = models.CharField(max_length=200)
    # The following field could be used to automate
    # exhibition labels or website summaries.
    # Spectrum 4.0 Brief description
    # VRA Core 4   description
    # DCMI         abstract
    # SICG         4.1 Descrição formal
    description = models.TextField()
    # Turn this into a fk for a bibliography model.
    # VRA Core 4   description_source
    description_source = models.CharField(max_length=200)
    # Spectrum 4.0 Comments
    # VRA Core 4   Append to description in output
    # SICG         Append to 4.1 Descrição formal in output
    comments = models.TextField()
    # Spectrum 4.0 Distinguishing features
    # VRA Core 4   Append to description in output
    # SICG         Append to 4.1 Descrição formal in output
    distinguishing_features = models.TextField()
    # Spectrum 4.0 Number of objects
    # DCMI         extent > count
    # SICG         3.4.2.1 Número de partes
    number_of_objects = models.PositiveIntegerField()

# Spectrum 4.0 Other object number
# SICG         7.4 Demais códigos
class OtherObjectNumber(models.Model):
    work_id = models.ForeignKey(ObjectIdentification, on_delete=models.CASCADE)
    other_object_number = models.CharField(max_length=72)
    other_object_number_type = models.CharField(max_length=200)

# Spectrum 4.0 Object name
# VRA Core 4   title
# DCMI         title
# SICG         1.3 Identificação do bem
class ObjectName(models.Model):
    work = models.ForeignKey(ObjectIdentification, on_delete=models.CASCADE)
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
    # To be populated with allowed name types as per VRA Core 4
    object_name_type = models.CharField(max_length=200)
# /Spectrum 4.0 Object identification information
###########################################################

###########################################################
# Spectrum 4.0 Object production information
# Simple fields grouped under the following class:
class ObjectProduction(models.Model):
    work = models.ForeignKey(ObjectIdentification, on_delete=models.CASCADE)
    # Sprvytum 4.0 Production organization, people, person
    # VRA Core 4   agent
    # DCMI         creator
    production_agent = models.ForeignKey(Agent, on_delete=models.PROTECT)
    # Spectrum 4.0 Production note
    # Not applicable in other standards?
    production_note = models.TextField()
    # Spectrum 4.0 Production place
    # VRA Core 4   location + location_type=creation
    # DCMI         spatial
    # SICG         2.3 Origem
    production_location = models.ForeignKey(GeographicLocation, on_delete=models.PROTECT)
    # The following field declares the original function served
    # by the object, that is, the justification for its production
    # Spectrum 4.0 Technical justification
    # VRA Core 4   Use a content field?
    technical_justification = models.TextField()
    # Spectrum 4.0 Technique type
    # VRA Core 4   tech_name
    # Not covered in DCMI
    # SICG         3.2 Técnicas
    technique_type = models.ForeignKey(TechniqueType, on_delete=models.PROTECT)

class TechniqueType(models.Model):
    # Spectrum 4.0 Technique
    # This field actually records the Trade to which
    # a specific Technique type belongs.
    # Use controlled vocab
    technique = models.CharField(max_length=64)
    # Use controlled vocab
    tecnique_type = models.CharField(max_length=200)
# /Spectrum 4.0 Object production information
###########################################################

###########################################################
# Spectrum 4.0 Object location information
# This group pertains only to locating an object in a
# collection, e.g. in a gallery or shelf.
# For places in the outside world, use GeographicLocation.
class ObjectLocation(models.Model):
    # Spectrum 4.0 Location
    # VRA Core 4   location, but only as pertaining to
    #              locating the object in the collection
    # DCMI         spatial, same caveat as above
    # Not available in SICG
    location = models.ForeignKey(AccessionLocation, on_delete=models.PROTECT)
    # Spectrum 4.0 Location fitness
    location_fitness = models.textField()
    # Spectrum 4.0 Location note
    location_note = models.textField()
    # The following field records the date the object
    # was moved to this location
    # Spectrum 4.0 Location date
    location_date = models.DateField()
    # Spectrum 4.0 Normal location
    normal_location = models.ForeignKey(AccessionLocation, on_delete=models.PROTECT)

class AccessionLocation(models.Model):
    # The physical address where this accession location resides.
    # Defaults to own organization, auto-fill from parent if exists:
    address = models.ForeignKey(GeographicLocation, on_delete=models.PROTECT)
    # The organization (or person, people) that owns the Geographic Location.
    # Defaults to own organization, auto-fill from parent if exists:
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT)
    # Locations can be recursive for maximum flexibility,
    # e.g. building > wing > room > furniture > shelf
    # or in any other way required by the organization.
    # Root-level locations will have this set to NULL:
    location_parent = models.ForeignKey(AccessionLocation, on_delete=models.PROTECT)
    location_id = models.CharField(max_length=7)
    # Keep the name short, follow conventions
    location_name = models.CharField(max_length=32)
    # Notes on the location or its name (e.g. "so-called", "condemned", etc.)
    location_note = models.TextField()
# /Spectrum 4.0 Object location information
###########################################################

###########################################################
# Spectrum 4.0 Object description information
# Simple description fields grouped under this class
# for convenience
class ObjectDescription(models.Model):
    # Spectrum 4.0 Physical description
    # VRA Core 4   description
    # DCMI         description
    physical_description = models.TextField()
    # colour to be replaced by fkey to controlled vocab
    # Meanwhile, prompt user to write comma-separated list
    # Spectrum 4.0 Colour
    # No equivalent in other standards
    colour = CharField(max_length=200)
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
# Dublin Core  contributor, creator, publisher
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

###########################################################
# General location information for use in several models
# Move to a specific application for integration with PostGIS
# and other metadata when project grows:
# Spectrum 4.0 several fields use this information
# VRA Core 4   location
# DCMI         spatial
class GeographicLocation(models.Model):
    None
# /VRA Core 4  location
###########################################################
