from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

###########################################################
# Spectrum 4.0 Object Identification Information
# VRA Core 4   work
# DCMI         Namespace root level
# SICG         1.3, 1.4, 3.4, 7.4
# This is the minimum required set of information to
# identify an object.
class ObjectIdentification(models.Model):
    # VRA Core 4   work, must prepend with 'w_' when rendering XML.
    # DCMI         identifier
    # This is NOT the object accession number but a unique identifier!
    # (See the VRA Core 4 spec for clarification)
    work_id = models.AutoField(max_length=7, primary_key=True)
    # Spectrum 4.0 Object number
    # VRA Core 4   refid
    # SICG         1.4 Código identificador Iphan
    # This IS the object accession number used in the organization.
    # The class that automates the creation of accession
    # numbers should be in a dedicated application,
    # so that it is more easily customized for each
    # organization.
    refid = models.OneToOneField('AccessionNumber', models.CASCADE, related_name='accession_number')
    # VRA Core 4   work > source
    # Default to own organization.
    source = models.CharField(max_length=200, default="My Museum", null=True, blank=True)
    # The following field could be used to automate
    # exhibition labels or website summaries.
    # Spectrum 4.0 Brief description
    # VRA Core 4   description, or not used?
    # DCMI         abstract
    # SICG         4.1 Descrição formal, or not used?
    description = models.TextField(null=True, blank=True)
    # Turn this into a fk for a bibliography model.
    # VRA Core 4   description_source
    description_source = models.CharField(max_length=200, null=True, blank=True)
    # Spectrum 4.0 Comments
    # VRA Core 4   work > notes
    # SICG         Append to 4.1 Descrição formal in output
    comments = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Distinguishing features
    # VRA Core 4   Append to description in output
    # SICG         Append to 4.1 Descrição formal in output
    distinguishing_features = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Number of objects
    # DCMI         extent > count
    # SICG         3.4.2.1 Número de partes
    # Best if this is computed from related objects,
    # rather than manually entered here.
    number_of_objects = models.PositiveIntegerField(default="1")

    def __str__(self):
        return refid + " " + self.objectname_set.filter(object_name_preferred=True)

# Spectrum 4.0 Other object number
# SICG         7.4 Demais códigos
class OtherObjectNumber(models.Model):
    object_identification = models.ForeignKey(ObjectIdentification, CASCADE)
    object_number = models.CharField(max_length=72)
    object_number_type = models.CharField(max_length=200)

    def __str__(self):
        return object_number_type + ': ' + object_number

# Spectrum 4.0 Object name
# VRA Core 4   title
# DCMI         title
# SICG         1.3 Identificação do bem
class ObjectName(models.Model):
    # Although artifacts can often have the same name,
    # every other metadata will be object-specific.
    object_identification = models.ForeignKey(ObjectIdentification, models.CASCADE)
    # The name itself:
    object_name = models.CharField(max_length=200)
    # Spectrum 4.0 Object name currency (i.e., as of when is it current?)
    # No equivalent in other standards
    object_name_currency = models.DateField(default=timezone.now, null=True, blank=True)
    # Spectrum 4.0 Object name level
    # Indicates at which level of a hierarchy this object is located,
    # e.g. is it a specimen, a genus, a group, etc.
    # Use controlled vocab
    object_name_level = models.CharField(max_length=64, null=True, blank=True)
    # Spectrum 4.0 Object name notes
    # VRA Core 4   title > note
    object_name_note = models.TextField(null=True, blank=True)
    # Spectrum 4.0 object name reference system
    # VRA Core 4   name > source
    # Eventually replace with fkey to bibliographic record
    object_name_source = models.CharField(max_length=200, null=True, blank=True)
    # VRA Core 4   title > xml:lang
    object_name_lang = models.ForeignKey(IsoLanguage, models.CASCADE)
    # Spectrum 4.0 Object name type
    # VRA Core 4   title > type
    object_name_type = models.PositiveSmallIntegerField(max_length=2, choices=object_name_type, default=3)
    # VRA Core 4   title > pref
    # DCMI         title.alternative
    # Spectrum 4.0 distinguishes between name and title
    # Best model practice is to render the Spectrum title field
    # when there is a title_type = creator
    object_name_preferred = models.BooleanField(default=False)
    # This should only be filled if there is a foreign-language
    # name of type 'creator' or 'inscribed'.
    # Eventually this should be handled by rendering
    # alternate language names.
    object_title_translation = models.CharField(max_length=200, null=True, blank=True)
    # VRA Core 4   work > title > type
    object_name_type = (
        (0, 'brandName'),
        (1, 'cited'),
        (2, 'creator'),
        (3, 'descriptive'),
        (4, 'former'),
        (5, 'inscribed'),
        (6, 'owner'),
        (7, 'popular'),
        (8, 'repository'),
        (9, 'translated'),
        (10, 'other'),
    )

    def __str__(self):
        return object_name
# /Spectrum 4.0 Object identification information
###########################################################

###########################################################
# Spectrum 4.0 Object production information
#
# VRA Core 4 has a more robust implementation for
# databases, breaking down this group into different
# actions, each of them with a 'creation' type---
# although this has loopholes, for example in
# allowing more than one 'creation' date_type.
# Spectrum prevents this problem even though this
# makes for inconsistent storage.
#
# We are tentatively implementing the Spectrum
# Object production information group as a class because
# it makes sense from a human reader point of view
# to have these informations grouped in one place.
#
# This class should only be active if the Object
# is of Artifact or IssuedObject type.
class ObjectProduction(models.Model):
    work = models.OneToOneField(ObjectIdentification, models.CASCADE)
    # Spectrum 4.0 Production date is a separate field
    #              from Description age
    # VRA Core 4   date + date_type=created
    # DCMI         created
    # SICG         2.1 Datação
    # While there can be rare occasions in which the same date set
    # applies to unrelated objects or events,
    # making it a one-to-one relationship keeps things cleaner,
    # even though inconsistent from a metadata-key point of view.
    production_date = models.OneToOneField(HistoricDate, models.PROTECT)
    # Spectrum 4.0 Production organization, people, person
    # VRA Core 4   agent + agent_type=creator
    # DCMI         creator
    production_agent = models.ForeignKey(Agent, models.PROTECT)
    # Spectrum 4.0 Production note
    # Not applicable in other standards?
    production_note = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Production place
    # VRA Core 4   location + location_type=creation
    # DCMI         spatial
    # SICG         2.3 Origem
    production_location = models.ForeignKey(Place, models.PROTECT)
    # The following field declares the original function served
    # by the object, that is, the justification for its production
    # Spectrum 4.0 Technical justification
    # VRA Core 4   Use a content field?
    technical_justification = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Technique type
    # VRA Core 4   tech_name
    # Not covered in DCMI
    # SICG         3.2 Técnicas
    technique_type = models.ManyToManyField(TechniqueType, models.PROTECT)

    def __str__(self):
        return 'Production information for object ' + ObjectIdentification.objects.filter(work_id=work)

class TechniqueType(models.Model):
    # Spectrum 4.0 Technique
    # Rather than an actual technique name,
    # this field in fact records the Trade to which
    # a specific Technique type belongs.
    # The most correct conceptual model would be to
    # have the Technique as a fkey to another class
    # containing the controlled vocab, but that would be
    # too unwieldy in practice.
    # Use controlled vocab
    technique = models.CharField(max_length=64)
    # Use controlled vocab
    tecnique_type = models.CharField(max_length=200)
    def __str__(self):
        return technique_type + " (" + technique + ")"
# /Spectrum 4.0 Object production information
###########################################################

###########################################################
# Spectrum 4.0 Object location information
# This group pertains only to locating an object in a
# collection, e.g. in a gallery or shelf.
# For places in the outside world, use Place.
class ObjectLocation(models.Model):
    work = models.ForeignKey(ObjectIdentification, models.CASCADE)
    # Spectrum 4.0 Location
    # VRA Core 4   location, but only as pertaining to
    #              locating the object in the collection
    # DCMI         spatial, same caveat as above
    # Not available in SICG
    location = models.ForeignKey(Location, models.PROTECT)
    # Spectrum 4.0 Location fitness
    # No equivalent in other standards.
    location_fitness = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Location note
    # VRA Core 4   location > notes
    location_note = models.TextField(null=True, blank=True)
    # The following field records the date the object
    # was moved to this location
    # Spectrum 4.0 Location date
    location_date = models.DateTimeField(default=timezone.now)
    # Spectrum 4.0 Normal location
    normal_location = models.ForeignKey(Location, models.PROTECT)

    def __str__(self):
        return 'Location information for object ' + ObjectIdentification.objects.filter(work_id=work)

class Location(models.Model):
    # Locations can be recursive for maximum flexibility,
    # e.g. building > wing > room > furniture > shelf
    # or in any other way required by the organization.
    # Root-level locations will have this set to NULL:
    location_parent = models.ForeignKey(Location, models.PROTECT, null=True, blank=True)
    # The physical address where this accession location resides.
    # Defaults to own organization, blank if inside a parent location.
    address = models.ForeignKey(Place, models.PROTECT, null=True, blank=True)
    # The organization (or person, people) that owns the Geographic Location.
    # Defaults to own organization, blank if inside a parent location.
    agent = models.ForeignKey(Agent, models.PROTECT, null=True, blank=True)
    # A code that identifies the location, if any.
    location_id = models.CharField(max_length=7, null=True, blank=True)
    # Keep the name short, follow conventions
    location_name = models.CharField(max_length=32)
    # Spectrum 4.0 Location note
    # VRA Core 4   location > notes
    # Notes on the location or its name (e.g. "so-called", "condemned", etc.)
    location_note = models.TextField(null=True, blank=True)

    def __str__(self):
        if location_parent:
            parent_string = ' in ' + location_parent
        else:
            parent_string = ''
        return location_id + ' ' + location_name + parent_string
# /Spectrum 4.0 Object location information
###########################################################

###########################################################
# Spectrum 4.0 Object description information
# We begin by separating the objects into three major
# classes which will have different descriptive fields.
# An Object type selector should activate only
# the appropriate class, if any, when creating
# an object record.
class Specimen(models.Model):
    # Biological specimens (live or preserved animals,
    # taxidermic work, fossils, etc.),
    # Geologic samples, and other natural objects.
    work = models.OneToOneField(ObjectIdentification, models.CASCADE, primary_key=True)
    # Spectrum 4.0 Age, age qualification, age unit
    geological_age = models.OneToOneField(HistoricDate, models.CASCADE, null=True, blank=True)
    # Biological age cannot use the HistoricDate class
    # and needs its own definition.
    specimen_age = models.PositiveIntegerField(null=True, blank=True)
    specimen_age_qualification = models.PositiveSmallIntegerField(max_length=1, default=0, choices=age_qualification_choice, null=True, blank=True)
    specimen_age_unit = models.PositiveSmallIntegerField(max_length=1, default=2, choices=age_unit_choice, null=True, blank=True)
    # No VRA Core 4 equivalent to Specimen
    # Biological phases, such as "larva" or "adult",
    # possibly also mineral information
    # Use controlled vocab
    phase = models.CharField(max_length=200, null=True, blank=True)
    sex = models.PositiveSmallIntegerField(max_length=1, default=0,  choices=sex_choice, null=True, blank=True)
    age_qualification_choice = (
        (0, ''),
        (1, 'around'),
        (2, 'less than'),
        (3, 'more than')
    )
    age_unit_choice = (
        (0, 'days'),
        (1, 'weeks'),
        (2, 'years'),
        (3, 'million years'),
        (4, 'billion years')
    )
    sex_choice = (
        (0, 'neuter'),
        (1, 'male'),
        (2, 'female'),
        (3, 'hermaphrodite'),
        (4, 'other')
    )

class Artifact(models.Model):
    # Pretty much everything else you would find in a museum.
    work = models.OneToOneField(ObjectIdentification, models.CASCADE, primary_key=True)
    # Spectrum 4.0 Object status
    # VRA Core 4   status
    # Indicates relationship of this object to others,
    # e.g. "copy," "counterfeit," "version," etc.
    # Use controlled vocab
    status = models.CharField(max_length=200, null=True, blank=True)
    # style to be replaced by fkey to controlled vocab
    # VRA Core 4  style_period
    # Dublin Core coverage
    # SICG        recorte temático
    style = models.CharField(max_length=200, null=True, blank=True)
    # Cultural Context to be replaced by fkey to controlled vocab
    # No Spectrum 4.0 equivalent for Cultural Context
    # VRA Core 4   cultural_context
    # DCMI         coverage
    # SICG         1.2 Recorte temático
    cultural_context = models.CharField(max_length=200, null=True, blank=True)

class IssuedObject(Artifact):
    # Printed material (books, engravings, etc.),
    # manuscript books, and so on.
    # Subclass of Artifact.
    # Copy number and Edition number will most often be integers,
    # but the fields can accommodate other explanations
    # as needed.
    # Spectrum 4.0 Copy number
    # VRA Core 4   issue_count
    copy_number = CharField(max_length=64, null=True, blank=True)
    # VRA Core 4  issue, issue_name
    # DCMI        issued
    edition_number = CharField(max_length=64, null=True, blank=True)
    # VRA Core 4  issue_type, issue_desc?
    # DCMI        hasFormat, stateEdition
    form = CharField(max_length=200, null=True, blank=True)
    # VRA Core 4  issue_source
    # No equivalent in other standards
    # To be replaced by fkey to bibliographic record
    issue_source = models.CharField(max_length=200, null=True, blank=True)

# Description fields common to all three object classes
# are grouped under this class.
class ObjectDescription(models.Model):
    work = models.ForeignKey(ObjectIdentification, models.CASCADE)
    # Spectrum 4.0 Physical description
    # VRA Core 4   Append to description in output,
    #              or standalone description,
    #              or not used?
    # DCMI         description
    physical_description = models.TextField(null=True, blank=True)
    # Spectrum 4.0 colour
    # Using a fkey to better organize controlled vocab,
    # but it's really a list of colors.
    # No equivalent in other standards
    colour = models.ManyToManyField(Colour, models.PROTECT)
    # territorial_context to be replaced by an advanced location app?
    # No Spectrum 4.0, VRA Core equivalent for territorial_context
    # SICG         1.1 Recorte territorial
    # DCMI         coverage
    # Use controlled vocab
    territorial_context = models.CharField(max_length=200, null=True, blank=True)
    # VRA Core 4 date
    # Not provided with this level of flexibility in other models,
    # as discussed in the HistoricDate class.
    date = models.ManyToManyField(HistoricDate, models.CASCADE, through=DateType)


# Spectrum 4.0 Colour
# No equivalent in other standards
class Colour(models.Model):
    # Use controlled vocab
    colour = models.CharField(max_length=200)
    def __str__(self):
        return colour

# Spectrum 4.0 can be used for Production date or Description age
# VRA Core 4   date
# DCMI         created, etc.
# SICG         Can be used with 2.1 Datação?
# Move to a dedicated application that can be machine read
# to produce timelines and comparisons: see theoretical model at
# http://www.museumsandtheweb.com/biblio/issues_in_historical_geography.html
class HistoricDate(models.Model):
    # The date model does not follow ISO-8601 due to this standard's
    # limitations for historical and fuzzy dates, which are
    # required in a museum context.
    date_earliest = models.PositiveIntegerField(max_length=7, null=True, blank=True)
    date_earliest_accuracy = models.PositiveSmallIntegerField(max_length=1, choices=date_accuracy, default=0)
    date_earliest_unit = models.PositiveIntegerField(max_length=2, choices=date_unit, default=0)
    date_earliest_qualifier = models.PositiveSmallIntegerField(max_length=1, choices=age_qualifier, default=1)
    date_latest = models.PositiveIntegerField(max_length=7, null=True, blank=True)
    date_latest_accuracy = models.PositiveSmallIntegerField(max_length=1, choices=date_accuracy, default=0)
    date_latest_unit = models.ForeignKey(AgeUnit, models.PROTECT)
    date_latest_qualifier = models.PositiveSmallIntegerField(max_length=1, choices=age_qualifier, default=1)
    date_source = models.CharField(max_length=200, null=True, blank=True)
    # Text representation of the date, for when more complex
    # explanations are required. If left blank, will be filled
    # with rendered concatenation of the previous fields
    # at a pre-save hook.
    date_text = models.CharField(max_length=200, null=True, blank=True)

    # VRA Core 4   only allows a True/False setting for 'circa'
    # Not provided in other standards.
    date_accuracy = (
        (0, ''),
        (1, 'before'),
        (2, 'up to'),
        (3, 'circa'),
        (4, 'after'),
        (5, 'from')
    )
    # No standard for date_unit
    date_unit = (
        (0, 'year'),
        (1, 'decade'),
        (2, 'quarter of century'),
        (3, 'third of century'),
        (4, 'half of century'),
        (5, 'century'),
        (6, 'quarter of millennium'),
        (7, 'third of millennium'),
        (8, 'half of millennium'),
        (9, 'millennium'),
        (10, 'million years'),
        (11, 'billion years')
    )
    # Spectrum 4.0 Age qualifier
    # B.P. should automatically render "age" instead of "date"
    age_qualifier = (
        (0, 'B.C.'),
        (1, 'A.D.'),
        (2, 'B.P.')
    )

    def __str__(self):
        return date_text

# VRA Core 4   date > type
# In VRA Core, 'date' is an attribute of any of the
# three root-level classes (work, agent, or image),
# and has distinct allowed date types accordingly.
# All other standards use a specific field for each date type,
# e.g. Spectrum 4.0 Production date, DCMI created, issued, etc.
class DateType(models.Model):
    # Date types in VRA Core are the types of events defined
    # by that date, e.g. creation, discovery, removal, etc.
    date_type = models.PositiveSmallIntegerField(max_length=2, choices=date_types)
    # VRA Core 4   date > source
    # Turn into fkey to bibliographic record
    date_source = models.CharField(max_length=200, null=True, blank=True)

    date_types = (
        (0, 'alteration'),
        (1, 'broadcast'),
        (2, 'bulk'),
        (3, 'commission'),
        (4, 'creation'),
        (5, 'design'),
        (6, 'destruction'),
        (7, 'discovery'),
        (8, 'exhibition'),
        (9, 'inclusive'),
        (10, 'performance'),
        (11, 'publication'),
        (12, 'restoration'),
        (13, 'view'),
        (14, 'other')
    )

# Spectrum 4.0 Content
# VRA Core 4   subject
# Dublin Core  subject
# This class should be a relationship manager
# whereas actual content should reside in
# type-specific classes.
class ObjectDescriptionContent(models.Model):
    # Most fields here will need careful review of the way
    # they are supposed to work in the Spectrum standard.
    # Spectrum 4.0 Content - activity
    # content_activity = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Content - concept
    # VRA Core 4   subj_type > content > conceptTopic
    # content_concept = models.
    # Spectrum 4.0 Content - date
    # VRA Core 4   date + (date_type != creation)
    # DCMI         several fields
    # content_date = models.ForeignKey(HistoricDate, models.CASCADE)
    # Spectrum 4.0 does not define a date_type field,
    # but it makes sense that it should have one.
    # VRA Core 4   date_type
    # content_description = models.
    # content_event_name = models. # for each a Content event name type
    # content_note = models.
    # content_object = models.ForeignKey(ObjectIdentification, models.PROTECT)
    # content_object needs content_object_type
    # Spectrum 4.0 renders content_organisation, content_people, and content_person
    # content_agent = models.ForeignKey(Agent, models.PROTECT)
    # content_place = models.ForeignKey(Place, models.PROTECT)
    # content_position = models.
    # content_other = models.
    pass

class ObjectDimension(models.Model):
    pass

class ObjectInscription(models.Model):
    pass

class ObjectMaterial(models.Model):
    pass

class TechnicalAttribute(models.Model):
    pass

class ObjectComponent(models.Model):
    pass
# /Spectrum 4.0 Object description information
###########################################################

###########################################################
# Move to a specific application for metadata when project grows:
# Spectrum 4.0 organization, people, person
# VRA Core 4   agent
# Dublin Core  contributor, creator, publisher
class Agent(models.Model):
    pass
# /Spectrum 4.0 organization, people, person
###########################################################

###########################################################
# Move to a specific application for metadata when project grows:
# Spectrum 4.0 Language
# VRA Core 4   xml:lang
# DCMI         language
class IsoLanguage(models.Model):
    language_iso = models.CharField(max_length=7)
    language = models.CharField(max_length=64)
# /Spectrum 4.0 Language
###########################################################

###########################################################
# General location information for use in several models
# Move to a specific application for integration with PostGIS
# and other metadata when project grows:
# Spectrum 4.0 several fields with 'place' data
# VRA Core 4   location
# DCMI         spatial
class Place(models.Model):
    pass
# /VRA Core 4  location
###########################################################
