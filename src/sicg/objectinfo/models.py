from django.db import models
from django.db.models import Count
from django.utils import timezone
from historicdate import HistoricDate, ObjectDateType

###########################################################
# Spectrum 4.0 Object Identification Information
# VRA Core 4   work
# DCMI         Namespace root level
# SICG M305    1.3, 1.4, 3.4, 7.4
# This is the minimum required set of information to
# identify an object.
class ObjectIdentification(models.Model):
    # VRA Core 4   work, must prepend with 'w_' when rendering XML.
    # DCMI         identifier
    # This is NOT the object accession number but a unique identifier!
    # (See the VRA Core 4 spec for clarification)
    work_id = models.AutoField(max_length=7, primary_key=True, editable=False)
    # This image is for quick reference purposes only,
    # to be photographed in the field when doing the
    # preliminary recording work.
    work_snapshot = models.ImageField()
    # Spectrum 4.0 Object number
    # VRA Core 4   refid
    # SICG M305    1.4 Código identificador Iphan
    # This IS the object accession number used in the organization.
    # The class that automates the creation of accession
    # numbers should be in a dedicated application,
    # so that it is more easily customized for each
    # organization.
    refid = models.OneToOneField('AccessionNumber', models.CASCADE, related_name='accession_number')
    # VRA Core 4   work > source
    # Source of knoledge regarding the work.
    source = models.CharField(max_length=200, null=True, blank=True)
    # The following field could be used to automate
    # exhibition labels or website summaries.
    # Spectrum 4.0 Brief description
    # VRA Core 4   description, or not used?
    # DCMI         abstract
    # SICG M305    4.1 Descrição formal, or not used?
    description = models.TextField(null=True, blank=True)
    # Turn this into a fk for a bibliography model.
    # VRA Core 4   description_source
    description_source = models.CharField(max_length=200, null=True, blank=True)
    # Spectrum 4.0 Comments
    # VRA Core 4   work > notes
    # SICG M305    Append to 4.1 Descrição formal in output
    comments = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Distinguishing features
    # VRA Core 4   Append to description in output
    # SICG M305    Append to 4.1 Descrição formal in output
    distinguishing_features = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Number of objects
    # DCMI         extent > count
    # SICG M305    3.4.2.1 Número de partes
    # Best if this is computed from related objects,
    # rather than manually entered here.
    # number_of_objects = models.PositiveIntegerField(default=1)
    # VRA Core 4   worktype
    # SICG M305    M301 Classificação do bem
    # Use controlled vocab
    work_type = CharField(max_length=200)

    def __str__(self):
        return refid + " " + self.objectname_set.filter(object_name_preferred=True)

# Spectrum 4.0 Other object number
# SICG M305    7.4 Demais códigos
class OtherObjectNumber(models.Model):
    work = models.ForeignKey(ObjectIdentification, models.CASCADE)
    object_number = models.CharField(max_length=72)
    object_number_type = models.CharField(max_length=200)

    def __str__(self):
        return object_number_type + ': ' + object_number

# Spectrum 4.0 Object name
# VRA Core 4   title
# DCMI         title
# SICG M305    1.3 Identificação do bem
class ObjectName(models.Model):
    # Although artifacts can often have the same name,
    # every other metadata will be object-specific.
    identification = models.ForeignKey(ObjectIdentification, models.CASCADE)
    # The name itself:
    object_name = models.CharField(max_length=200)
    # Spectrum 4.0 Object name currency (i.e., as of when is it current?)
    # No equivalent in other standards
    name_currency = models.DateField(default=timezone.now, null=True, blank=True)
    # Spectrum 4.0 Object name level
    # Indicates at which level of a hierarchy this object is located,
    # e.g. is it a specimen, a genus, a group, etc.
    # Use controlled vocab
    name_level = models.CharField(max_length=64, null=True, blank=True)
    # Spectrum 4.0 Object name notes
    # VRA Core 4   title > note
    name_note = models.TextField(null=True, blank=True)
    # Spectrum 4.0 object name reference system
    # VRA Core 4   name > source
    # Eventually replace with fkey to bibliographic record
    name_source = models.CharField(max_length=200, null=True, blank=True)
    # VRA Core 4   title > xml:lang
    name_lang = models.ForeignKey(IsoLanguage, models.CASCADE)
    # Spectrum 4.0 Object name type
    # VRA Core 4   title > type
    name_type = models.PositiveSmallIntegerField(max_length=2, choices=title_type, default=3)
    # VRA Core 4   title > pref
    # DCMI         title.alternative
    # Spectrum 4.0 distinguishes between name and title
    # Best model practice is to render the Spectrum title field
    # when there is a title_type = creator
    name_preferred = models.BooleanField(default=False)
    # This should only be filled if there is a foreign-language
    # name of type 'creator' or 'inscribed'.
    # Eventually this should be handled by rendering
    # alternate language names.
    title_translation = models.CharField(max_length=200, null=True, blank=True)

    # VRA Core 4   work > title > type
    title_type = (
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
# is of Artifact or ArtifactInstance type.
class ObjectProduction(models.Model):
    work = models.OneToOneField(ObjectIdentification, models.CASCADE)
    # Spectrum 4.0 Production date is a separate field
    #              from Description age
    # VRA Core 4   date + date_type=created
    # DCMI         created
    # SICG M305    2.1 Datação
    # While there can be rare occasions in which the same date set
    # applies to unrelated objects or events,
    # making it a one-to-one relationship keeps things cleaner,
    # even though inconsistent from a metadata-key point of view.
    production_date = models.OneToOneField(historicdate.HistoricDate, models.PROTECT)
    # Spectrum 4.0 Production organization, people, person
    # VRA Core 4   agent + agent_type=creator
    # DCMI         creator
    production_agent = models.ManyToManyField(Agent, models.PROTECT, through='Roles')
    # Spectrum 4.0 Production note
    # VRA Core 4   Will have a notes field for each of
    # 'agent > creator', 'date > created', and so on.
    production_note = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Production place
    # VRA Core 4   location + location_type=creation
    # DCMI         spatial
    # SICG M305    2.3 Origem
    production_location = models.ForeignKey(Place, models.PROTECT)
    # The following field declares the original function served
    # by the object, that is, the justification for its production
    # Spectrum 4.0 Technical justification
    # VRA Core 4   Use a content field?
    technical_justification = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Technique type
    # VRA Core 4   tech_name
    # Not covered in DCMI
    # SICG M305    3.2 Técnicas
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
    tecnique_type = models.CharField(max_length=200, unique=True)
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
# This is the most complex information group in Spectrum,
# and the most inconsistent across different standards,
# so modeling must be careful to account for all the
# required information while making sure it can be
# exchanged properly.
#
# We begin by separating the objects into three major
# classes which will have different descriptive fields.
# An Object type selector should activate only
# the appropriate class when creating an object record.
#
# First we create an abstract meta-class to be referenced
# by each of the three object types.
# Simple Description fields common to all three object classes
# are grouped under this class for convenience.
class ObjectDescription(models.Model):
    # Object description is strictly bound to its respective
    # Object identification, so much so that we only split
    # the two groups to remain consistent with the Spectrum
    # standard, and also to make each class easier to manage.
    work = models.OneToOneField(ObjectIdentification, models.CASCADE, primary_key=True)
    # Spectrum 4.0 Physical description
    # VRA Core 4   Append to description in output,
    #              or standalone description,
    #              or not used?
    # DCMI         description
    # SICG M305    4.1 Descrição formal
    physical_description = models.TextField(null=True, blank=True)
    # Spectrum 4.0 colour
    # Using a fkey to better organize controlled vocab,
    # but it's really a list of colors.
    # No equivalent in other standards
    colour = models.ManyToManyField(Colour, models.PROTECT)
    # Strictly speaking, Territorial context is only required
    # by SICG, so consider removing it because it only
    # functions in a very specific context of nationwide
    # heritage management. Any one museum should have no need
    # to specify several territorial contexts and ought
    # rather to rely on style_period and cultural_context.
    # No Spectrum 4.0, VRA Core equivalent for territorial_context
    # SICG M305    1.1 Recorte territorial
    # DCMI         coverage
    # Use controlled vocab
    # territorial_context = models.CharField(max_length=200, null=True, blank=True)
    #
    # VRA Core 4 date
    # Not provided with this level of flexibility in other models,
    # as discussed in the historicdate.HistoricDate class.
    object_date = models.ManyToManyField(historicdate.HistoricDate, models.CASCADE, through=historicdate.ObjectDateType)
    # Spectrum 4.0 Material
    # VRA Core 4   material
    # SICG M305    3.1 Materiais
    material = models.ManyToManyField(ObjectMaterial, models.PROTECT, through=MaterialType)
    # The field that picks up content (Spectrum) / subject (VRA Core) items
    # into the object description.
    description_content = models.ManyToManyField(DescriptionContent, models.PROTECT, through=ContentMeta, null=True, blank=True)
    # The textual description of the content, as required by Spectrum
    # and allowed by VRA Core 4.
    description_display = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

# Biological specimens (live or preserved animals,
# taxidermic work, fossils, etc.),
# Geologic samples, and other natural objects.
class Specimen(ObjectDescription):
    # Spectrum 4.0 Age, age qualification, age unit
    # Biological age cannot use the HistoricDate class
    # and needs its own definition.
    specimen_age = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    specimen_age_qualification = models.PositiveSmallIntegerField(max_length=1, default=0, choices=age_qualification_choice, null=True, blank=True)
    specimen_age_unit = models.PositiveSmallIntegerField(max_length=1, default=2, choices=age_unit_choice, null=True, blank=True)
    # No VRA Core 4 equivalent to Specimen
    # Biological phases, such as "larva" or "adult",
    # as well as textual description of age.
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
        (2, 'years')
    )
    sex_choice = (
        (0, 'neuter'),
        (1, 'male'),
        (2, 'female'),
        (3, 'hermaphrodite'),
        (4, 'other')
    )

# Pretty much everything else you would find in a museum.
class Artifact(ObjectDescription):
    # Spectrum 4.0 Object status
    # VRA Core 4   status
    # Indicates relationship of this object to others,
    # e.g. "copy," "counterfeit," "version," etc.
    # Use controlled vocab
    status = models.CharField(max_length=200, null=True, blank=True)
    # style to be replaced by fkey to controlled vocab
    # Spectrum 4.0 Style
    # VRA Core 4   style_period
    # Dublin Core  coverage
    # SICG M305    7.1 Características estilísticas
    style = models.CharField(max_length=200, null=True, blank=True)
    # Cultural Context to be replaced by fkey to controlled vocab
    # No Spectrum 4.0 equivalent for Cultural Context
    # VRA Core 4   cultural_context
    # DCMI         coverage
    # SICG M305    1.2 Recorte temático
    cultural_context = models.CharField(max_length=200, null=True, blank=True)

# Printed material (books, engravings, etc.),
# photographs, and other objects that can have originals in
# several instances. Subclass of Artifact.
class WorkInstance(Artifact):
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

# Spectrum 4.0 Colour
# No equivalent in other standards
class Colour(models.Model):
    # Use controlled vocab
    colour = models.CharField(max_length=200, unique)
    def __str__(self):
        return colour

# Spectrum 4.0 Content
# VRA Core 4   subject
# Dublin Core  subject
# SICG M305    7.2 Características iconográficas
class DescriptionContent(models.Model):
    content_name = models.CharField()
    content_type = models.PositiveSmallIntegerField(max_length=2, choices=content_types)
    content_types = (
        # First, the VRA Core 4 types
        ('Agent', (
            (0, 'corporateName'),
            (1, 'familyName'),
            (2, 'otherName'),
            (3, 'personalName')
        ) )
        ('Object', (
            (4, 'scientificName') # For Spectrum, contained in content > object
        ) )
        ('Place', (
            (5, 'builtWorkPlace'),
            (6, 'geographicPlace'),
            (7, 'otherPlace')
        ) )
        ('Topic', (
            (8, 'conceptTopic'),
            (9, 'descriptiveTopic'),
            (10, 'iconographicTopic'),
            (11, 'otherTopic')
        ) )
        # Fill with remaining Spectrum 4.0 categories
        ('Other', (
            (12, 'activity'),
            (13, 'date'),
            (14, 'event name'),
            (14, 'note')
        ) )
    )

# The content itself is distinguished from its metadata
# because a piece of content is a keyword that can occur in
# several works, but the metadata is how that content is
# applied on the specific object.
class ContentMeta(models.Model):
    object = models.ForeignKey(ObjectDescription, models.CASCADE)
    content = models.ForeignKey(DescriptionContent, models.PROTECT)
    # Spectrum 4.0 object type
    object_type = models.CharField(max_length=64, null=True, blank=True)
    # Spectrum 4.0 event type
    event_type = models.CharField(max_length=64, null=True, blank=True)
    # Spectrum 4.0 other type
    other_type = models.CharField(max_length=64, null=True, blank=True)
    # Spectrum 4.0 content script
    content_script = models.CharField(max_length=200, null=True, blank=True)
    # Spectrum 4.0 content language
    content_lang = models.ForeignKey(IsoLanguage, models.PROTECT, null=True, blank=True)
    # Spectrum 4.0 content position. Can be null because it might cover
    # the entire work.
    content_position = models.CharField(max_length=64, null=True, blank=True)
    # Spectrum 4.0 content note
    # VRA Core 4   content > source
    content_source = models.CharField(max_length=200, null=True, blank=True)

# Spectrum 4.0 Object dimension
# VRA Core 4   Measurements
# DCMI         extent
# SICG M305    3.3 Dimensões
class ObjectDimension(models.Model):
    work = models.ForeignKey(ObjectIdentification, models.CASCADE)
    # Spectrum 4.0 Dimension measured part
    # VRA Core 4   measurements > extent
    # Use controlled vocab
    dimension_part = models.CharField(max_length=32)
    # VRA Core 4   measurements > type
    # Other standards mix up 'part' and 'type',
    # the latter of which is properly height, length,
    # weight, etc.
    dimension_type = models.PositiveSmallIntegerField(max_length=2, default=11, choices=measurement_type)
    # Spectrum 4.0 Dimension value
    # VRA Core 4   measurements (root)
    # DCMI         fields according to dimension_type
    dimension_value = models.PositiveIntegerField()
    # Spectrum 4.0 Dimension value date
    # VRA Core 4   measurements > dataDate
    dimension_value_date = models.DateField(default=timezone.now)
    # Spectrum 4.0 Dimension value qualifier
    # Not provided in VRA Core or DCMI
    # SICG M305    3.3.1 Precisa / 3.3.2 Aproximada
    # False = exact measurement, True = approximate measurement
    dimension_value_qualifier = models.BooleanField(default=False)

    measurement_type = (
        # Spectrum 4.0 Dimension measurement unit is implicit
        # from the measurement type chosen, to make
        # things simpler.
        # Fields below provided by VRA Core 4.
        (0, 'area (cm²)'),
        (1, 'base (mm)'), # Obviously inconsistent with what VRA Core distinguishes as measurement type vs. measurement extent, keep track to see if they fix this in a future version.
        # (2, 'bit-depth'),            # Spectrum Technical attribute measurement
        (3, 'circumference (mm)'),
        (4, 'count'),
        (5, 'depth (mm)'),
        (6, 'diameter (mm)'),
        # (7, 'distanceBetween (mm)'), # Spectrum Technical attribute measurement
        # (8, 'duration (s)'),         # Spectrum Technical attribute measurement
        # (9, 'fileSize (kB)'),        # Spectrum Technical attribute measurement
        (10, 'height (mm)'),
        (11, 'length (mm)'),
        # (12, 'resolution (ppi)'),    # Spectrum Technical attribute measurement
        # (13, 'runningTime (s)'),     # Spectrum Technical attribute measurement
        # (14, 'scale'),               # Spectrum Technical attribute measurement
        # (15, 'size'),                # Spectrum Technical attribute measurement
        # (16, 'target'),              # Spectrum Technical attribute measurement
        (17, 'weight (g)'),
        (18, 'width (mm)'),
        # (19, 'other')                # Spectrum Technical attribute measurement
    )

# Spectrum 4.0 Inscription
# VRA Core 4   Inscription
# SICG M305    4.2 Marcas e inscrições
class ObjectInscription(models.Model):
    # Although there can be rare cases of identical
    # inscriptions on different objects, for the sake of
    # conceptual consistency (each inscription is marked
    # on one specific artifact), let's make it a
    # one-to-one relationship.
    work = models.OneToOneField(ObjectIdentification, models.CASCADE)
    # Spectrum 4.0 Inscription content | Inscription description
    # VRA Core 4   Inscription > [display]
    # If left blank, will be auto-filled (or rendered?) based on
    # other fields below.
    inscription_display = models.TextField(null=True, blank=True)
    # Spectrum 4.0 fills out
    # different fields if it is a textual or graphic
    # inscription, yet also sets a 'type'
    # VRA Core 4   inscription > type
    # Graphic inscription will usually fall under 'other'.
    inscription_type = models.PositiveSmallIntegerField(max_length=1, default=0, choices=inscription_types)
    # Spectrum 4.0 Inscriber
    # VRA Core 4   inscription > author
    inscription_author = models.ForeignKey(Agent, models.PROTECT, null=True, blank=True)
    # Spectrum 4.0 Inscription date
    # VRA Core 4   Not explicitly defined, but conceptually
    # available at inscription > date.
    inscription_date = models.OneToOneField(historicdate.HistoricDate, models.CASCADE, null=True, blank=True)
    # Spectrum 4.0 Inscription interpretation
    # VRA Core 4   Not explicitly defined, but conceptually
    # available at inscription > notes
    inscription_notes = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Inscription language
    # VRA Core 4   xml:lang
    inscription_language = models.ForeignKey(IsoLanguage, models.PROTECT, null=True, blank=True)
    # Spectrum 4.0 Inscription method
    # VRA Core 4   No specific field, usage is to put
    # this information in the 'position' field.
    # Strictly speaking this should not be allowed to be
    # left blank, since every inscription has a method,
    # but it might be easier for preliminary entry to leave
    # it blank and fill out later with better research.
    inscription_method = models.ForeignKey(TechniqueType, models.PROTECT, null=True, blank=True)
    # Spectrum 4.0 Inscription position
    # VRA Core 4   inscription > position
    # A descriptive text, but using controlled vocab
    # whenever possible.
    inscription_position = models.CharField(max_length=200)
    # Spectrum 4.0 Inscription script
    # VRA Core 4   Not defined, presumably derived from xml:lang
    # Use controlled vocab, leave blank if not writing.
    inscription_script = models.CharField(max_length=64, null=True, blank=True)
    # Spectrum 4.0 Does not define this field explicitly
    # VRA Core 4   Caveat: since it is an XML format, the
    # 'inscription > text' field should use the transliterated value,
    # if it exists.
    # Leave blank if the inscription does not contain writing.
    inscription_text = models.CharField(null=True, blank=True)
    # Best practice for museums that display information in
    # several languages would be to define another model
    # 'InscriptionText' with a fkey to the Inscription model;
    # this way, there can be as many translations and
    # transliterations as needed.
    # Spectrum 4.0 Inscription transliteration
    # VRA Core 4   inscription > text (for the reasons
    # explained in 'inscription_text')
    # Leave blank if the inscription does not contain writing
    # or does not require transliteration.
    inscription_transliteration = models.CharField(null=True, blank=True)
    # Spectrum 4.0 Inscription translation
    # VRA Core 4   Defined as a second 'inscription > text'
    # field with the corresponding 'xml:lang' attribute.
    inscription_translation = models.CharField(null=True, blank=True)

    inscription_types = (
        (0, 'signature'),
        (1, 'mark'),
        (2, 'caption'),
        (3, 'date'),
        (4, 'text'),
        (5, 'translation'),
        (6, 'other')
    )

# Spectrum 4.0 Material
# VRA Core 4   material
# SICG M305    3.1 Materiais
class ObjectMaterial(models.Model):
    # Spectrum 4.0 Material component
    # No equivalent in other standards
    # Only input information based on technical analysis.
    material_component = models.CharField(max_length=64, null=True, blank=True)
    # Spectrum 4.0 Material component note
    # VRA Core 4   material > notes
    material_note = models.CharField(null=True, blank=True)
    # Spectrum 4.0 Material name
    # VRA Core 4   material
    # Common name for apparent material, based on visual
    # inspection. This is the only required field in this class.
    # Use controlled vocab.
    material_name = models.CharField(max_length=200)
    # Spectrum 4.0 Material source
    # No equivalent in other standards
    # Geographic origin of material, if known.
    material_source = models.ForeignKey(Place, models.PROTECT, null=True, blank=True)
    # VRA Core 4 requires an ID field for each material,
    # linked to a controlled vocabulary.
    # Can be activated by uncommenting the following line.
    # material_refid = models.IntegerField(max_length=9, primary_key=True, editable=True)

class MaterialType(models.Model):
    material_type = models.PositiveSmallIntegerField(max_length=1, default=0, choices=material_types)
    material = models.ForeignKey(models.ObjectMaterial, models.PROTECT)
    work = models.ForeignKey(models.ObjectIdentification, models.CASCADE)
    # VRA Core 4   material > extent
    # Not defined in other standards.
    # Use only if needed to distinguish different parts
    # in distinct materials.
    material_extent = models.CharField(max_length=200, null=True, blank=True)

    # VRA Core 4   material > type
    material_types = (
        (0, 'medium'),
        (1, 'support'),
        (2, 'other')
    )

# Spectrum 4.0 Technical attribute
# VRA Core 4   The nature of the information that Spectrum
# requests as a technical attribute is provided by VRA
# Core 4 in the 'measurements' group.
class TechnicalAttribute(models.Model):
     work = models.ForeignKey(ObjectIdentification, models.CASCADE)
     # Spectrum 4.0 Technical attribute
     # VRA Core 4   measurements > type
     # Other standards mix up 'part' and 'type',
     # the latter of which is properly height, length,
     # weight, etc.
     attribute_type = models.PositiveSmallIntegerField(max_length=2, default=11, choices=attribute_types)
     # Spectrum 4.0 Technical attribute measurement
     # VRA Core 4   measurements (root)
     # DCMI         fields according to dimension_type
     attribute_value = models.PositiveIntegerField()

     attribute_types = (
         # Spectrum 4.0 Technical attribute measurement unit is implicit
         # from the measurement type chosen, to make
         # things simpler.
         # Fields below provided by VRA Core 4.
         # (0, 'area (cm²)'),           # Spectrum Dimension
         # (1, 'base (mm)'),            # Spectrum Dimension
         (2, 'bit-depth'),            # Spectrum Technical attribute measurement
         # (3, 'circumference (mm)'),   # Spectrum Dimension
         # (4, 'count'),                # Spectrum Dimension
         # (5, 'depth (mm)'),           # Spectrum Dimension
         # (6, 'diameter (mm)'),        # Spectrum Dimension
         (7, 'distanceBetween (mm)'), # Spectrum Technical attribute measurement
         (8, 'duration (s)'),         # Spectrum Technical attribute measurement
         (9, 'fileSize (kB)'),        # Spectrum Technical attribute measurement
         # (10, 'height (mm)'),         # Spectrum Dimension
         # (11, 'length (mm)'),         # Spectrum Dimension
         (12, 'resolution (ppi)'),    # Spectrum Technical attribute measurement
         (13, 'runningTime (s)'),     # Spectrum Technical attribute measurement
         (14, 'scale'),               # Spectrum Technical attribute measurement
         (15, 'size'),                # Spectrum Technical attribute measurement
         (16, 'target'),              # Spectrum Technical attribute measurement
         # (17, 'weight (g)'),          # Spectrum Dimension
         # (18, 'width (mm)'),          # Spectrum Dimension
         (19, 'other')                # Spectrum Technical attribute measurement
     )

# Spectrum 4.0 Object component
# Description of non-removable parts of an object
# (for removable parts, number each part individually
# in an Object Identification group and describe them
# as separate objects).
# This class should only be activated if needed for a
# particularly complex object, otherwise it adds
# too much complexity to the entry process.
# class ObjectComponent(models.Model):
#     pass
# /Spectrum 4.0 Object description information
###########################################################

###########################################################
# Spectrum 4.0 Object rights information group
# VRA Core 4   rights
# DCMI         license
# SICG M305    5. Situação jurídica
# This is distinct from the 'Object *rights in*
# information' group, which declares rights granted on
# the object by a third party.
class ObjectRights(models.Model):
    work = models.ForeignKey(ObjectIdentification, models.CASCADE)
    # Spectrum 4.0 right begin date
    right_begin_date = models.DateField(null=True, blank=True)
    # Spectrum 4.0 right end date
    right_end_date = models.DateField(null=True, blank=True)
    # Spectrum 4.0 Right holder
    # VRA Core 4   rights > rightsHolder
    rights_holder = models.ManyToManyField(Agent, models.PROTECT, null=True, blank=True)
    # VRA Core 4   rights > text
    rights_display = models.CharField(max_length=200)
    # Spectrum 4.0 Right notes
    # VRA Core 4   rights > notes
    rights_notes = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Right reference number
    # Not defined in other standards. Made editable in case
    # someone needs to write a custom contract number, for
    # example, but handle with care.
    rights_refid = models.AutoField(max_length=7, primary_key=True, editable=True)
    # Spectrum 4.0 Right type
    # VRA Core 4   rights > type
    rights_type = models.PositiveSmallIntegerField(max_length=1, default=0, choices=rights_types)

    rights_types = (
        (0, 'copyrighted'),
        (1, 'publicDomain'),
        (2, 'undetermined'),
        (3, 'other')
    )
# /Spectrum 4.0 Object rights information group
###########################################################

###########################################################
# Spectrum 4.0 Object history and association information
# Will eventually have the following information:
# Spectrum 4.0 Associated activity
# Spectrum 4.0 Associated activity note
# Spectrum 4.0 Associated concept
# Spectrum 4.0 Associated cultural affinity
# Spectrum 4.0 Associated date
# Spectrum 4.0 Associated event date
# Spectrum 4.0 Associated event name
# Spectrum 4.0 Associated event name type
# Spectrum 4.0 Associated event organisation/people/person
# Spectrum 4.0 Associated event place

# Spectrum 4.0 Associated object
# SICG M305    6. Documentos relacionados
# Tentatively being used to record documents and sources
# with detail that object_source cannot have.
class AssociatedObject(models.Model):
    work = models.ForeignKey(ObjectIdentification, models.CASCADE)
    associated_object_name = models.CharField(max_length=200)
    # Spectrum 4.0 Associated object type
    # SCIG M305    Formato do arquivo
    # Use a simple term, preferably from controlled vocab
    associated_object_type = models.CharField(max_length=64)
    associated_object_datadate = models.DateField(default=timezone.now)

# Spectrum 4.0 Associated organisation/people/person
# Spectrum 4.0 Associated place
# Spectrum 4.0 Association note
# Spectrum 4.0 Association type
# Spectrum 4.0 Object history note

# Spectrum 4.0 owner/ownership
# SICG M305    5. Estatuto jurídico (inconsistently)
# Not defined in VRA Core 4, DCMI
# Designed to hold information abou previous ownership
# conditions, not current policies, since it is assumed
# the object is owned by the home organisation.
# However, CIDOC/ICOM recommends current information be
# recorded so it can be made available to others.
# SICG requires both information on current ownership
# as well as the last recorded owner.
class Ownership(models.Model):
    # Spectrum 4.0 Owner organisation/person (not people)
    # Defaults to own organization.
    owner = models.ForeignKey(Agent, models.PROTECT, default="My Museum")
    # Spectrum 4.0 Ownership access
    # Names the access restriction in place.
    # Spectrum 4.0 Ownership category
    # Use standardized vocabulary, preferred values are
    # 'public,' 'private,' and 'corporate.'
    owner_category = models.PositiveSmallIntegerField(max_length=1, default=0, choices=owner_categories)
    # Spectrum 4.0 Ownership dates
    # As per VRA Core 4.0, blank dates should be rendered
    # as 'present' in the output.
    owner_begin_date = models.DateField(null=True, blank=True)
    owner_end_date = models.DateField(null=True, blank=True)
    # Spectrum 4.0 Ownership exchange method
    owner_method = models.PositiveSmallIntegerField(max_length=1, default=0, choices=owner_methods)
    # Spectrum 4.0 Ownership exchange note
    owner_note = models.TextField(null=True, blank=True)
    # Spectrum 4.0 Ownership exchange price
    owner_price = models.DecimalField(max_length=11, null=True, blank=True)
    # Spectrum 4.0 Ownership place
    owner_place = models.ForeignKey(Place, models.PROTECT, null=True, blank=True)

    # SICG M301 3. Propriedade
    owner_categories = (
        (0, 'public'),
        (1, 'private'),
        (2, 'mixed'),
        (3, 'other')
    )

    # 'Lease' is of course not a method of transfer of
    # ownership, but it is provided here for compatibility
    # with the SICG standard.
    owner_methods = (
        (0, 'purchase'),
        (1, 'lease'),
        (2, 'donation'),
        (3, 'other')
    )

# Spectrum 4.0 Related object
# VRA Core 4   relation
# Dublin Core  relation
# SICG M305    3.5 Objetos relacionados
# This is distinct from the subject > object
# field, in that it records objects related to one
# another, rather than an object referred to in
# another object.
class RelatedObject(models.Model):
    # Spectrum 4.0 Related object number
    # VRA Core 4   relid
    # Read as 'work1' 'related_association' 'work2'
    work1 = models.ForeignKey(ObjectIdentification, models.CASCADE)
    work2 = models.ForeignKey(ObjectIdentification, models.CASCADE)
    # Spectrum 4.0 Related object association
    # The type of association between the objects (copy, model,
    # representation, etc.)
    relation_type = models.PositiveSmallIntegerField(max_length=2, choices=relation_types)
    # Spectrum 4.0 Related object note
    related_note = models.TextField(null=True, blank=True)

    # VRA Core 4
    # There are duplicate relations for two-way rendering,
    # make sure they are identified as each other's reverse.
    # Can we do this without having a separate through-class
    # for each pair of associations?
    relation_types = (
        ('default', (
            (37, "relatedTo"),
        ) )
        ('hierarchical', (
            (25, "partOf"),
            (26, "largerContextFor"),
            (18, "formerlyPartOf"),
            (19, "formerlyLargerContextFor"),
        ))
        ('components', (
            (2, "componentOf"),
            (3, "componentIs"),
        ))
        ('steps', (
            (0, "cartoonFor"),
            (1, "cartoonIs"),
            (6, "counterProofFor"),
            (7, "counterProofIs"),
            (23, "modelFor"),
            (24, "modelIs"),
            (29, "planFor"),
            (30, "planIs"),
            (31, "prepatoryFor"),
            (32, "basedOn"),
            (33, "printingPlateFor"),
            (34, "printingPlateIs"),
            (35, "prototypeFor"),
            (36, "prototypeIs"),
            (38, "reliefFor"),
            (39, "impressionIs"),
            (42, "studyFor"),
            (43, "studyIs"),
        ))
        ('together', (
            (12, "designedFor"),
            (13, "contextIs"),
            (14, "exhibitedAt"), # Not an object-to-object relation
            (15, "venueFor"),    # Not an object-to-object relation
            (22, "mateOf"),
            (27, "partnerInSetWith"),# Not an object-to-object relation
            (28, "pendantOf"),
        ))
        ('after', (
            (4, "copyAfter"),
            (5, "copyIs"),
            (8, "depicts"),
            (9, "depictedIn"),
            (10, "derivedFrom"),
            (11, "sourceFor"),
            (16, "facsimileOf"),
            (17, "facsimileIs"),
            (40, "replicaOf"),
            (41, "replicaIs"),
            (44, "versionOf"),
            (45, "versionIs")
        ))
        ('image', (
            (20, "imageOf"),
            (21, "imageIs"),
        ))
    )

# Spectrum 4.0 Usage
# Spectrum 4.0 Usage note
# /Spectrum 4.0 Object history and association information
###########################################################

###########################################################
# VRA Core 4   textref
# SICG M305    7.3 Referência bibliográfica e arquivística
# This group primarly intended to record the object in
# catalogues and where it gets other reference numbers.
class TextRef(models.Model):
    # Because the TextRef includes a specific citation
    # to the object, it will not be reusable in other
    # objects' records, therefore not Many-to-Many.
    work = models.ForeignKey(ObjectIdentification, models.CASCADE)
    # Eventually render the name from a bibliographic
    # database record.
    textref_name = models.CharField(max_length=200)
    textref_name_type = models.CharField(max_length=16, default='book', choices=textref_name_types)
    # If the reference provides a different number for
    # the object, or a citation, record it here:
    textref_refid = models.CharField(max_length=64, null=True, blank=True)
    textref_refid_type = models.PositiveSmallIntegerField(max_length=1, default=0, choices=textref_refid_types)
    # Date when the information was located
    textref_datadate = models.DateF(default=timezone.now)
    # Required by SICG:
    textref_location = models.ForeignKey(Place, models.PROTECT)

    textref_name_types = (
        ('book', 'Book'),
        ('catalog', 'Catalog'),
        ('corpus', 'Corpus'),
        ('electronic', 'Electronic format'),
        ('serial', 'Serial'),
        ('other', 'Other')
    )

    textref_refid_types = (
        ('citation', 'Citation'),
        ('openURL', 'OpenURL'),
        ('isbn', 'ISBN'),
        ('issn', 'ISSN'),
        ('uri', 'URI'),
        ('vendor', 'Vendor reference'),
        ('other', 'Other')
    )
# /VRA Core 4   textref
###########################################################

###########################################################
# Move to a specific application for metadata when project grows:
# Spectrum 4.0 Language
# VRA Core 4   xml:lang
# DCMI         language
class IsoLanguage(models.Model):
    language_iso = models.CharField(max_length=7, primary_key=True)
    language = models.CharField(max_length=64, unique=True)
# /Spectrum 4.0 Language
###########################################################

###########################################################
# A number of other groups defined by Spectrum 4.0 as
# 'Object ... groups' are actually procedure information.
# Therefore, they will not be included in this application,
# but rather in a separate Object Procedure app.
# These include:
# - Object audit information
# - Object conservation and treatment information
# - Object valuation information
# - Object viewer's contribution information
###########################################################
