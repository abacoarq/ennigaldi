from django.db import models
from django.db.models import Count
from django.utils import timezone
from historicdate.models import HistoricDate, DateType
from agent.models import Agent
from place.models import Place, PlaceType
from storageunit.models import Unit

###########################################################
# Spectrum 4.0 Object Identification Information
# VRA Core 4   work
# DCMI         Namespace root level
# SICG M305    1.3, 1.4, 3.4, 7.4
# This is the minimum required set of information to
# identify an object.
class ObjectRegister(models.Model):
    work_types = (
            ('artifact', 'Artifact'),
            ('issuedObject', 'Issued Object'),
            ('specimen', 'Specimen'),
        )
    # VRA Core 4   work, must prepend with 'w_' when rendering XML.
    # DCMI         identifier
    # This is NOT the object accession number but a unique identifier!
    # (See the VRA Core 4 spec for clarification)
    work_id = models.AutoField(max_length=7, primary_key=True, editable=False)
    # This image is for quick reference purposes only,
    # to be photographed in the field when doing the
    # preliminary recording work.
    snapshot_height = models.CharField(max_length=15, blank=True)
    snapshot_width = models.CharField(max_length=15, blank=True)
    snapshot = models.ImageField(upload_to='media/w_snapshot/', height_field='snapshot_height', width_field='snapshot_width', max_length=255, blank=True, null=True)
    # This field helps compute the correct accession number
    # in case it requires objects that are part of a set
    # to have a single number appended with a part number.
    # It should be populated from an "add part" button in
    # the parent object page rather than filled manually.
    hierarchy = models.ManyToManyField("self", related_name='has_part', symmetrical=False, through='Hierarchy', through_fields=('lesser', 'greater'))
    # Spectrum 4.0 Object number
    # VRA Core 4   refid
    # SICG M305    1.4 Código identificador Iphan
    # This IS the object accession number used in the organization.
    # The class that automates the creation of accession
    # numbers should be in a dedicated application,
    # so that it is more easily customized for each
    # organization.
    # To be filled automatically by the function that saves
    # the object.
    # It must be allowed to be blank because the object
    # must be saved first for the refid generation to work
    # with object part detection.
    # This is being auto-generated at save time and is modeled
    # in the Accession Number application for optimal
    # flexibility.
    # refid = models.OneToOneField(AccessionNumber, models.PROTECT, related_name='refid_of', editable=False, blank=True)
    #
    # Spectrum 4.0 Object name
    # VRA Core 4   title > pref
    # DCMI         title
    preferred_title = models.OneToOneField('ObjectName', models.CASCADE)
    # VRA Core 4   worktype
    # SICG M305    M301 Classificação do bem
    # Use controlled vocab
    work_type = models.CharField(max_length=31, choices=work_types, default='artifact')
    # VRA Core 4   work > source
    # Source of knoledge regarding the work.
    source = models.CharField(max_length=255, blank=True)
    # The following field could be used to automate
    # exhibition labels or website summaries.
    # Spectrum 4.0 Brief description
    # VRA Core 4   description, or not used?
    # DCMI         abstract
    # SICG M305    4.1 Descrição formal, or not used?
    brief_description = models.TextField(blank=True)
    # Turn this into a fk for a bibliography model.
    # VRA Core 4   description_source
    description_source = models.CharField(max_length=255, blank=True)
    # Spectrum 4.0 Comments
    # VRA Core 4   work > notes
    # SICG M305    Append to 4.1 Descrição formal in output
    comments = models.TextField(blank=True)
    # Spectrum 4.0 Distinguishing features
    # VRA Core 4   Append to description in output?
    # SICG M305    Append to 4.1 Descrição formal in output
    distinguishing_features = models.TextField(blank=True)
    # Spectrum 4.0 Number of objects
    # DCMI         extent > count
    # SICG M305    3.4.2.1 Número de partes
    # Complementary information is split into different
    # classes according to their Spectrum 4.0 information
    # groups, so as to make the whole easier to manage.
    production = models.OneToOneField('Production', models.PROTECT, null=True, blank=True)
    storage_unit = models.ManyToManyField('storageunit.Unit', related_name='%(app_label)s_storage_for_%(class)s', through='ObjectUnit')
    # Spectrum 4.0 Normal location
    normal_unit = models.ForeignKey('storageunit.Unit', models.PROTECT, null=True)

    def __str__(self):
        wid = str(self.work_id)
        return 'w_' + wid.zfill(7) + ' ' + self.preferred_title.__str__()

    def is_part(self):
        q = Hierarchy.objects.filter(lesser__pk=self.pk, relation_type=('partOf' or  'componentOf'))
        if q:
            return q.values_list(greater__pk, flat=True)[0]

    def has_parts(self):
        q = Hierarchy.objects.filter(greater__pk=self.pk, relation_type=('partOf' or 'componentOf'))
        if q:
            return q.values_list(lesser__pk, flat=True)

# Spectrum 4.0 Other object number
# SICG M305    7.4 Demais códigos
class OtherNumber(models.Model):
    work = models.ForeignKey('ObjectRegister', models.CASCADE)
    object_number = models.CharField(max_length=71)
    object_number_type = models.CharField(max_length=255)

    def __str__(self):
        return object_number_type + ': ' + object_number

# Spectrum 4.0 Object name, Title
# VRA Core 4   title
# DCMI         title, title.alternative
# SICG M305    1.3 Identificação do bem
# Spectrum 4.0 distinguishes between name and title
# Best model practice is to render the Spectrum title field
# when there is a title_type = creator?
class ObjectName(models.Model):
    # VRA Core 4   work > title > type
    title_type = (
        ('brandName', 'brand name'),
        ('cited', 'cited as'),
        ('creator', 'given by creator'),
        ('descriptive', 'descriptive'),
        ('former', 'former'),
        ('inscribed', 'inscribed'),
        ('owner', 'given by owner'),
        ('popular', 'popular'),
        ('repository', 'used in repository'),
        ('translated', 'translated'),
        ('other', 'other'),
    )
    # work = models.ForeignKey('ObjectRegister', models.CASCADE)
    # The name itself:
    title = models.CharField(max_length=255)
    # Spectrum 4.0 Object name currency (i.e., as of when is it current?)
    # No equivalent in other standards
    currency = models.DateField(default=timezone.now, blank=True)
    # Spectrum 4.0 Object name level
    # Indicates at which level of a hierarchy this object is located,
    # e.g. is it a specimen, a genus, a group, etc.
    # Use controlled vocab
    level = models.CharField(max_length=63, blank=True)
    # Spectrum 4.0 Object name notes
    # VRA Core 4   title > note
    note = models.TextField(blank=True)
    # Spectrum 4.0 object name reference system
    # VRA Core 4   name > source
    # Eventually replace with fkey to bibliographic record
    source = models.CharField(max_length=255, blank=True)
    # VRA Core 4   title > xml:lang
    lang = models.ForeignKey('IsoLanguage', models.CASCADE)
    # Spectrum 4.0 Object name type
    # VRA Core 4   title > type
    title_type = models.CharField(max_length=15, choices=title_type, default='descriptive')
    # This should only be filled if there is a foreign-language
    # name of type 'creator' or 'inscribed'.
    # Eventually this should be handled by rendering
    # alternate language names.
    translation = models.CharField(max_length=255, blank=True)

    # class Meta:
        # unique_together = ('work', 'title')

    def __str__(self):
        if len(self.translation) > 1:
            return self.translation
        else:
            return self.title
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
# This class should only be active if the Object
# is of Artifact or ArtifactInstance type.
class Production(models.Model):
    # Spectrum 4.0 Production date is a separate field
    #              from Description age
    # VRA Core 4   date + date_type=created
    # DCMI         created
    # SICG M305    2.1 Datação
    # While there can be rare occasions in which the same date set
    # applies to unrelated objects or events,
    # making it a one-to-one relationship keeps things cleaner,
    # even though inconsistent from a metadata-key point of view.
    date = models.OneToOneField(HistoricDate, models.PROTECT)
    # Spectrum 4.0 Production organization, people, person
    # VRA Core 4   agent + agent_type=creator
    # DCMI         creator
    agent = models.ManyToManyField('agent.Agent', through='AgentRole', related_name='%(app_label)s_agent_for_%(class)s')
    # Spectrum 4.0 Production note
    # VRA Core 4   Will have a notes field for each of
    # 'agent > creator', 'date > created', and so on.
    note = models.TextField(blank=True)
    # Spectrum 4.0 Production place
    # VRA Core 4   location + location_type=creation
    # DCMI         spatial
    # SICG M305    2.3 Origem
    location = models.ManyToManyField('place.Place', related_name='%(app_label)s_location_for_%(class)s', through='ObjectPlaceType')
    # The following field declares the original function served
    # by the object, that is, the justification for its production
    # Spectrum 4.0 Technical justification
    # VRA Core 4   Use a content field?
    technical_justification = models.TextField(blank=True)
    technique_type = models.ManyToManyField("TechniqueType", related_name='%(app_label)s_technique_in_%(class)s')

    def __str__(self):
        return 'Production information for object ' + ObjectRegister.objects.filter(work_id=self.work).__str__()

class AgentRole(models.Model):
    agent = models.ForeignKey('agent.Agent', models.PROTECT, related_name='has_agent')
    work = models.ForeignKey('Production', models.PROTECT, related_name='agent_of_work')
    # VRA Core 4 agent > role
    # Use controlled vocab
    agent_role = models.CharField(max_length=31)
    # 'False' means the work is securely known, e.g. from a
    # signature, while 'True' means it is attributed.
    attributed = models.BooleanField(default=False)
    attribution_type = models.CharField(max_length=31, blank=True)
    # Optional field to record complex attribution.
    # If left blank, a pre-save hook should render it from
    # the information provided above.
    agent_role_display = models.CharField(max_length=255)

    def __str__(self):
        return agent_role_display

class ObjectPlaceType(PlaceType):
    work = models.ForeignKey('Production', models.PROTECT)

# SICG M305    3.2 Técnicas
# Spectrum 4.0 Technique
# Rather than an actual technique name,
# this field in fact records the Trade to which
# a specific Technique type belongs.
# The most correct conceptual model would be to
# have the Technique as a fkey to another class
# containing the controlled vocab, but that would be
# too unwieldy in practice.
# Use controlled vocab
class TechniqueType(models.Model):
    technique = models.CharField(max_length=64, blank=True)
    # Spectrum 4.0 Technique type
    # VRA Core 4   tech_name
    # Not covered in DCMI
    # Use controlled vocab
    tecnique_type = models.CharField(max_length=255, blank=True)

    def __str__():
        return technique + ': ' + technique_type
# /Spectrum 4.0 Object production information
###########################################################

###########################################################
# Spectrum 4.0 Object location information
# This group pertains only to locating an object in a
# collection, e.g. in a gallery or shelf.
# For places in the outside world, use Place.
class ObjectUnit(models.Model):
    work = models.ForeignKey('ObjectRegister', models.CASCADE, related_name='objects_in_location')
    # Spectrum 4.0 Location
    # VRA Core 4   location, but only as pertaining to
    #              locating the object in the collection
    # DCMI         spatial, same caveat as above
    # Not available in SICG
    unit = models.ForeignKey('storageunit.Unit', models.PROTECT, related_name='contains_objects')
    # Spectrum 4.0 Location fitness
    # No equivalent in other standards.
    fitness = models.TextField(blank=True)
    # Spectrum 4.0 Location note
    # VRA Core 4   location > notes
    note = models.TextField(blank=True)
    # The following field records the date the object
    # was moved to this location
    # Spectrum 4.0 Location date
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.work.__str__() + ' located in ' + self.unit.__str__()
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
class Description(models.Model):
    work = models.OneToOneField('ObjectRegister', models.CASCADE)
    # Spectrum 4.0 Physical description
    # VRA Core 4   Append to description in output,
    #              or standalone description,
    #              or not used?
    # DCMI         description
    # SICG M305    4.1 Descrição formal
    physical_description = models.TextField(blank=True)
    # Spectrum 4.0 colour
    # Using a fkey to better organize controlled vocab,
    # but it's really a list of colors.
    # No equivalent in other standards
    colour = models.ManyToManyField('Colour', related_name='%(app_label)s_colour_in_%(class)s')
    dimension = models.ManyToManyField('Dimension', related_name='+')
    technical_attribute = models.ManyToManyField('TechnicalAttribute', related_name='+')
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
    # territorial_context = models.CharField(max_length=255, blank=True)
    #
    # The textual description of the content, as required by Spectrum
    # and allowed by VRA Core 4.
    description_display = models.TextField(blank=True)

    class Meta:
        abstract = True

# Biological specimens (live or preserved animals,
# taxidermic work, fossils, etc.),
# Geologic samples, and other natural objects.
class Specimen(Description):
    age_qualification_choice = (
        ('exact', 'exact'),
        ('around', 'around'),
        ('lessThan', 'less than'),
        ('moreThan', 'more than')
    )
    age_unit_choice = (
        ('days', 'days'),
        ('weeks', 'weeks'),
        ('years', 'years')
    )
    sex_choice = (
        ('neuter', 'neuter'),
        ('male', 'male'),
        ('female', 'female'),
        ('hermaphrodite', 'hermaphrodite'),
        ('other', 'other')
    )
    # Spectrum 4.0 Age, age qualification, age unit
    # Biological age cannot use the HistoricDate class
    # and needs its own definition.
    specimen_age = models.DecimalField(max_digits=5, decimal_places=1, blank=True)
    specimen_age_qualification = models.CharField(max_length=15, default='exact', choices=age_qualification_choice, blank=True)
    specimen_age_unit = models.CharField(max_length=15, default='years', choices=age_unit_choice, blank=True)
    # No VRA Core 4 equivalent to Specimen
    # Biological phases, such as "larva" or "adult",
    # as well as textual description of age.
    # Use controlled vocab
    phase = models.CharField(max_length=255, blank=True)
    sex = models.CharField(max_length=15, default='male',  choices=sex_choice, blank=True)
    # VRA Core 4 date
    # Not provided with this level of flexibility in other models,
    # as discussed in the historicdate.HistoricDate class.
    object_date = models.ManyToManyField('historicdate.HistoricDate', related_name='%(app_label)s_date_for_%(class)s', through='SpecimenDateType')

# Pretty much everything else you would find in a museum.
class Artifact(Description):
    # Spectrum 4.0 Object status
    # VRA Core 4   status
    # Indicates relationship of this object to others,
    # e.g. "copy," "counterfeit," "version," etc.
    # Use controlled vocab
    status = models.CharField(max_length=255, blank=True)
    # style to be replaced by fkey to controlled vocab
    # Spectrum 4.0 Style
    # VRA Core 4   style_period
    # Dublin Core  coverage
    # SICG M305    7.1 Características estilísticas
    style = models.CharField(max_length=255, blank=True)
    # Cultural Context to be replaced by fkey to controlled vocab
    # No Spectrum 4.0 equivalent for Cultural Context
    # VRA Core 4   cultural_context
    # DCMI         coverage
    # SICG M305    1.2 Recorte temático
    cultural_context = models.CharField(max_length=255, blank=True)
    # The field that picks up content (Spectrum) / subject (VRA Core) items
    # into the object description.
    description_content = models.ManyToManyField('DescriptionContent', related_name='%(app_label)s_content_in_%(class)s', through='ContentMeta', blank=True)
    # Spectrum 4.0 Material
    # VRA Core 4   material
    # SICG M305    3.1 Materiais
    material = models.ManyToManyField('Material', related_name='%(app_label)s_material_in_%(class)s', through='MaterialType')
    # VRA Core 4 date
    # Not provided with this level of flexibility in other models,
    # as discussed in the historicdate.HistoricDate class.
    object_date = models.ManyToManyField('historicdate.HistoricDate', related_name='%(app_label)s_date_for_%(class)s', through='ArtifactDateType')

# Printed material (books, engravings, etc.),
# photographs, and other objects that can have originals in
# several instances. Subclass of Artifact.
class WorkInstance(Artifact):
    # Copy number and Edition number will most often be integers,
    # but the fields can accommodate other explanations.
    # Spectrum 4.0 Copy number
    # VRA Core 4   issue_count
    copy_number = models.CharField(max_length=63, blank=True)
    # VRA Core 4  issue, issue_name
    # DCMI        issued
    edition_number = models.CharField(max_length=63, blank=True)
    # VRA Core 4  issue_type, issue_desc?
    # DCMI        hasFormat, stateEdition
    work_form = models.CharField(max_length=255, blank=True)
    # VRA Core 4  issue_source
    # No equivalent in other standards
    # To be replaced by fkey to bibliographic record
    issue_source = models.CharField(max_length=255, blank=True)

# Spectrum 4.0 Object dimension
# VRA Core 4   Measurements
# DCMI         extent
# SICG M305    3.3 Dimensões
class Dimension(models.Model):
    measurement_type = (
        # Spectrum 4.0 Dimension measurement unit is implicit
        # from the measurement type chosen, to make
        # things simpler.
        # Fields below provided by VRA Core 4.
        ('area', 'area (cm²)'),
        ('base', 'base (mm)'), # Obviously inconsistent with what VRA Core distinguishes as measurement type vs. measurement extent, keep track to see if they fix this in a future version.
        # ('bit-depth', 'bit-depth'),            # Spectrum Technical attribute measurement
        ('circumference', 'circumference (mm)'),
        ('count', 'count'),
        ('depth', 'depth (mm)'),
        ('diameter', 'diameter (mm)'),
        # ('distanceBetween (mm)', 'distanceBetween (mm)'), # Spectrum Technical attribute measurement
        # ('duration (s)', 'duration (s)'),         # Spectrum Technical attribute measurement
        # ('fileSize (kB)', 'fileSize (kB)'),        # Spectrum Technical attribute measurement
        ('height', 'height (mm)'),
        ('length', 'length (mm)'),
        # ('resolution (ppi)', 'resolution (ppi)'),    # Spectrum Technical attribute measurement
        # ('runningTime (s)', 'runningTime (s)'),     # Spectrum Technical attribute measurement
        # ('scale', 'scale'),               # Spectrum Technical attribute measurement
        # ('size', 'size'),                # Spectrum Technical attribute measurement
        # ('target', 'target'),              # Spectrum Technical attribute measurement
        ('weight', 'weight (g)'),
        ('width', 'width (mm)'),
        # ('other', 'other')                # Spectrum Technical attribute measurement
    )
    work = models.ForeignKey('ObjectRegister', models.CASCADE)
    # Spectrum 4.0 Dimension measured part
    # VRA Core 4   measurements > extent
    # Use controlled vocab
    dimension_part = models.CharField(max_length=32)
    # VRA Core 4   measurements > type
    # Other standards mix up 'part' and 'type',
    # the latter of which is properly height, length,
    # weight, etc.
    dimension_type = models.CharField(max_length=31, default='length', choices=measurement_type)
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

# Spectrum 4.0 Inscription
# VRA Core 4   Inscription
# SICG M305    4.2 Marcas e inscrições
class Inscription(models.Model):
    inscription_types = (
            ('signature', 'Signature'),
            ('mark', 'Mark or symbol'),
            ('caption', 'Caption'),
            ('date', 'Date'),
            ('translation', 'Translation'),
            ('text', 'Other text'),
            ('other', 'Other inscription'),
    )
    work = models.ForeignKey(ObjectRegister, models.CASCADE)
    # Spectrum 4.0 Inscription content | Inscription description
    # VRA Core 4   Inscription > [display]
    # If left blank, will be auto-filled (or rendered?) based on
    # other fields below.
    inscription_display = models.TextField(blank=True)
    # Spectrum 4.0 fills out
    # different fields if it is a textual or graphic
    # inscription, yet also sets a 'type'
    # VRA Core 4   inscription > type
    # Graphic inscription will usually fall under 'other'.
    inscription_type = models.CharField(max_length=15, choices=inscription_types)
    # Spectrum 4.0 Inscriber
    # VRA Core 4   inscription > author
    inscription_author = models.ForeignKey('agent.Agent', models.PROTECT, blank=True)
    # Spectrum 4.0 Inscription date
    # VRA Core 4   Not explicitly defined, but conceptually
    # available at inscription > date.
    inscription_date = models.OneToOneField('historicdate.HistoricDate', models.CASCADE, blank=True)
    # Spectrum 4.0 Inscription interpretation
    # VRA Core 4   Not explicitly defined, but conceptually
    # available at inscription > notes
    inscription_notes = models.TextField(blank=True)
    # Spectrum 4.0 Inscription language
    # VRA Core 4   xml:lang
    inscription_language = models.ForeignKey('IsoLanguage', models.PROTECT, blank=True, null=True)
    # Spectrum 4.0 Inscription method
    # VRA Core 4   No specific field, usage is to put
    # this information in the 'position' field.
    # Strictly speaking this should not be allowed to be
    # left blank, since every inscription has a method,
    # but it might be easier for preliminary entry to leave
    # it blank and fill out later with better research.
    inscription_method = models.ForeignKey('TechniqueType', models.PROTECT, blank=True)
    # Spectrum 4.0 Inscription position
    # VRA Core 4   inscription > position
    # A descriptive text, but using controlled vocab
    # whenever possible.
    inscription_position = models.CharField(max_length=255)
    # Spectrum 4.0 Inscription script
    # VRA Core 4   Not defined, presumably derived from xml:lang
    # Use controlled vocab, leave blank if not writing.
    inscription_script = models.CharField(max_length=63, blank=True)
    # Spectrum 4.0 Does not define this field explicitly
    # VRA Core 4   Caveat: since it is an XML format, the
    # 'inscription > text' field should use the transliterated value,
    # if it exists.
    # Leave blank if the inscription does not contain writing.
    inscription_text = models.TextField(blank=True)
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
    inscription_transliteration = models.TextField(blank=True)
    # Spectrum 4.0 Inscription translation
    # VRA Core 4   Defined as a second 'inscription > text'
    # field with the corresponding 'xml:lang' attribute.
    inscription_translation = models.TextField(blank=True)

# Spectrum 4.0 Technical attribute
# VRA Core 4   The nature of the information that Spectrum
# requests as a technical attribute is provided by VRA
# Core 4 in the 'measurements' group.
class TechnicalAttribute(models.Model):
     attribute_types = (
         # Spectrum 4.0 Technical attribute measurement unit is implicit
         # from the measurement type chosen, to make
         # things simpler.
         # Fields below provided by VRA Core 4.
         # ('area (cm²)', 'area (cm²)'),           # Spectrum Dimension
         # ('base (mm)', 'base (mm)'),            # Spectrum Dimension
         ('bit-depth', 'bit-depth'),            # Spectrum Technical attribute measurement
         # ('circumference (mm)', 'circumference (mm)'),   # Spectrum Dimension
         # ('count', 'count'),                # Spectrum Dimension
         # ('depth (mm)', 'depth (mm)'),           # Spectrum Dimension
         # ('diameter (mm)', 'diameter (mm)'),        # Spectrum Dimension
         ('distanceBetween', 'distance between (mm)'), # Spectrum Technical attribute measurement
         ('duration', 'duration (s)'),         # Spectrum Technical attribute measurement
         ('fileSize', 'file size (kB)'),        # Spectrum Technical attribute measurement
         # ('height (mm)', 'height (mm)'),         # Spectrum Dimension
         # ('length (mm)', 'length (mm)'),         # Spectrum Dimension
         ('resolution', 'resolution (ppi)'),    # Spectrum Technical attribute measurement
         ('runningTime', 'running time (s)'),     # Spectrum Technical attribute measurement
         ('scale', 'scale'),               # Spectrum Technical attribute measurement
         ('size', 'size'),                # Spectrum Technical attribute measurement
         ('target', 'target'),              # Spectrum Technical attribute measurement
         # ('weight (g)', 'weight (g)'),          # Spectrum Dimension
         # ('width (mm)', 'width (mm)'),          # Spectrum Dimension
         ('other', 'other')                # Spectrum Technical attribute measurement
     )
     work = models.ForeignKey('ObjectRegister', models.CASCADE)
     # Spectrum 4.0 Technical attribute
     # VRA Core 4   measurements > type
     # Other standards mix up 'part' and 'type',
     # the latter of which is properly height, length,
     # weight, etc.
     attribute_type = models.CharField(max_length=31, default='fileSize', choices=attribute_types)
     # Spectrum 4.0 Technical attribute measurement
     # VRA Core 4   measurements (root)
     # DCMI         fields according to dimension_type
     attribute_value = models.PositiveIntegerField()

# Spectrum 4.0 Colour
# No equivalent in other standards
class Colour(models.Model):
    # Use controlled vocab
    colour = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return colour

class SpecimenDateType(DateType):
    dated = models.ForeignKey('Specimen', models.CASCADE, related_name='dated_specimen')

class ArtifactDateType(DateType):
    dated = models.ForeignKey('Artifact', models.CASCADE, related_name='dated_artifact')

# Spectrum 4.0 Material
# VRA Core 4   material
# SICG M305    3.1 Materiais
class Material(models.Model):
    # Spectrum 4.0 Material component
    # No equivalent in other standards
    # Only input information based on technical analysis.
    material_component = models.CharField(max_length=63, blank=True)
    # Spectrum 4.0 Material component note
    # VRA Core 4   material > notes
    material_note = models.CharField(max_length=255, blank=True)
    # Spectrum 4.0 Material name
    # VRA Core 4   material
    # Common name for apparent material, based on visual
    # inspection. This is the only required field in this class.
    # Use controlled vocab.
    material_name = models.CharField(max_length=255)
    # Spectrum 4.0 Material source
    # No equivalent in other standards
    # Geographic origin of material, if known.
    material_source = models.ForeignKey('place.Place', models.PROTECT, blank=True, null=True)
    # VRA Core 4 requires an ID field for each material,
    # linked to a controlled vocabulary.
    # Can be activated by uncommenting the following line.
    # material_refid = models.IntegerField(primary_key=True, editable=True)

    def __str__(self):
        return self.material_name

class MaterialType(models.Model):
    # VRA Core 4   material > type
    material_types = (
        ('medium', 'medium'),
        ('support', 'support'),
        ('other', 'other')
    )
    material_type = models.CharField(max_length=15, default='medium', choices=material_types)
    material = models.ForeignKey('Material', models.PROTECT)
    work = models.ForeignKey('Artifact', models.CASCADE)
    # VRA Core 4   material > extent
    # Not defined in other standards.
    # Use only if needed to distinguish different parts
    # in distinct materials.
    material_extent = models.CharField(max_length=255, blank=True)

# Spectrum 4.0 Content
# VRA Core 4   subject
# Dublin Core  subject
# SICG M305    7.2 Características iconográficas
class DescriptionContent(models.Model):
    content_types = (
        # First, the VRA Core 4 types
        ('Agent', (
            ('corporateName', 'corporate name'),
            ('familyName', 'family or group name'),
            ('otherName', 'other name'),
            ('personalName', 'personal name')
        ) ),
        ('Object', (
            ('scientificName', 'scientific name') # For Spectrum, contained in content > object
        ) ),
        ('Place', (
            ('builtWorkPlace', 'location of a built work'),
            ('geographicPlace', 'geographic location'),
            ('otherPlace', 'other location')
        ) ),
        ('Topic', (
            ('conceptTopic', 'concept topic'),
            ('descriptiveTopic', 'descriptive topic'),
            ('iconographicTopic', 'iconographic topic'),
            ('otherTopic', 'other topic')
        ) ),
        # Fill with remaining Spectrum 4.0 categories
        ('Other', (
            ('activity', 'activity'),
            ('date', 'date'),
            ('eventName', 'event name'),
            ('note', 'note')
        ) ),
    )
    content_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=31, choices=content_types)

# The content itself is distinguished from its metadata
# because a piece of content is a keyword that can occur in
# several works, but the metadata is how that content is
# applied on the specific object.
class ContentMeta(models.Model):
    work = models.ForeignKey('Artifact', models.CASCADE)
    content = models.ForeignKey('DescriptionContent', models.PROTECT)
    # Spectrum 4.0 object type
    object_type = models.CharField(max_length=63, blank=True)
    # Spectrum 4.0 event type
    event_type = models.CharField(max_length=63, blank=True)
    # Spectrum 4.0 other type
    other_type = models.CharField(max_length=63, blank=True)
    # Spectrum 4.0 content script
    content_script = models.CharField(max_length=255, blank=True)
    # Spectrum 4.0 content language
    content_lang = models.ForeignKey('IsoLanguage', models.PROTECT, blank=True)
    # Spectrum 4.0 content position
    # Can be blank because it might cover the entire work.
    content_position = models.CharField(max_length=63, blank=True)
    # Spectrum 4.0 content note
    # VRA Core 4   content > source
    content_source = models.CharField(max_length=255, blank=True)


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
class Rights(models.Model):
    rights_types = (
        ('copyrighted', 'copyrighted'),
        ('publicDomain', 'public domain'),
        ('undetermined', 'undetermined'),
        ('other', 'other')
    )
    work = models.ForeignKey('ObjectRegister', models.CASCADE)
    # Spectrum 4.0 right begin date
    right_begin_date = models.DateField(blank=True)
    # Spectrum 4.0 right end date
    right_end_date = models.DateField(blank=True)
    # Spectrum 4.0 Right holder
    # VRA Core 4   rights > rightsHolder
    rights_holder = models.ManyToManyField('agent.Agent', related_name='has_rights', blank=True)
    # VRA Core 4   rights > text
    rights_display = models.CharField(max_length=255)
    # Spectrum 4.0 Right notes
    # VRA Core 4   rights > notes
    rights_notes = models.TextField(blank=True)
    # Spectrum 4.0 Right reference number
    # Not defined in other standards. Made editable in case
    # someone needs to write a custom contract number, for
    # example, but handle with care.
    rights_refid = models.AutoField(max_length=7, primary_key=True, editable=True)
    # Spectrum 4.0 Right type
    # VRA Core 4   rights > type
    rights_type = models.CharField(max_length=15, default='undetermined', choices=rights_types)
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
    work = models.ForeignKey('ObjectRegister', models.CASCADE)
    associated_object_name = models.CharField(max_length=255)
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
# Designed to hold information about previous ownership
# conditions, not current policies, since it is assumed
# the object is owned by the home organisation.
# However, CIDOC/ICOM recommends current information be
# recorded so it can be made available to others.
# SICG requires both information on current ownership
# as well as the last recorded owner.
class Ownership(models.Model):
    # SICG M301 3. Propriedade
    ownership_categories = (
        ('public', 'public'),
        ('private', 'private'),
        ('mixed', 'mixed'),
        ('other', 'other')
    )
    # 'Lease' is of course not a method of transfer of
    # ownership, but it is provided here for compatibility
    # with the SICG standard.
    ownership_methods = (
        ('purchase', 'purchase'),
        ('lease', 'lease'),
        ('donation', 'donation'),
        ('other', 'other')
    )
    # Spectrum 4.0 Owner organisation/person (not people)
    # Defaults to own organization.
    owner = models.ForeignKey('agent.Agent', models.PROTECT, default="My Museum")
    # Spectrum 4.0 Ownership access
    # Names the access restriction in place.
    # Spectrum 4.0 Ownership category
    # Use standardized vocabulary, preferred values are
    # 'public,' 'private,' and 'corporate.'
    ownership_category = models.CharField(max_length=15, default='public', choices=ownership_categories)
    # Spectrum 4.0 Ownership dates
    # As per VRA Core 4.0, blank dates should be rendered
    # as 'present' in the output.
    ownership_begin_date = models.DateField(blank=True)
    ownership_end_date = models.DateField(blank=True)
    # Spectrum 4.0 Ownership exchange method
    ownership_method = models.CharField(max_length=15, default='purchase', choices=ownership_methods)
    # Spectrum 4.0 Ownership exchange note
    ownership_note = models.TextField(blank=True)
    # Spectrum 4.0 Ownership exchange price
    sale_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True)
    # Spectrum 4.0 Ownership place
    ownership_place = models.ForeignKey('place.Place', models.PROTECT, blank=True)

# Spectrum 4.0 Related object
# VRA Core 4   relation
# Dublin Core  relation
# SICG M305    3.5 Objetos relacionados
# This is distinct from the subject > object
# field, in that it records objects related to one
# another, rather than an object referred to in
# another object.
# The Related object field is being split into two
# separate classes to handle two distinct situations:
# - hierarchical relationships (ForeignKey);
# - multiple relationships (ManyToMany).
class Hierarchy(models.Model):
    relation_types = (
        # Commented-out fields are established by VRA Core 4 but
        # must be derived from the inverse database relationship
        # rather than set explicitly.
        ('hierarchical', (
            ('partOf', 'part of'),
            # ('largerContextFor', 'larger context for'),
            ('formerlyPartOf', 'formerly part of'),
            # ('formerlyLargerContextFor', 'formerly larger context for'),
            ('componentOf', 'component of'),
            # ('componentIs', 'component is'),
        )),
        ('steps', (
            ('cartoonFor', 'cartoon for'),
            # ('cartoonIs', 'cartoon is'),
            ('counterProofFor', 'counter proof for'),
            # ('counterProofIs', 'counter proof is'),
            ('modelFor', 'model for'),
            # ('modelIs', 'model is'),
            ('planFor', 'plan for'),
            # ('planIs', 'plan is'),
            ('prepatoryFor', 'prepatory for'),
            # ('basedOn', 'based on'),
            ('printingPlateFor', 'printing plate for'),
            # ('printingPlateIs', 'printing plate is'),
            ('prototypeFor', 'prototype for'),
            # ('prototypeIs', 'prototype is'),
            ('reliefFor', 'relief for'),
            # ('impressionIs', 'impression is'),
            ('studyFor', 'study for'),
            # ('studyIs', 'study is'),
        )),
        ('after', (
            ('copyAfter', 'copy after'),
            # ('copyIs', 'copy is'),
            ('facsimileOf', 'facsimile of'),
            # ('facsimileIs', 'facsimile is'),
            ('replicaOf', 'replica of'),
            # ('replicaIs', 'replica is'),
            ('versionOf', 'version of'),
            # ('versionIs', 'version is')
        )),
        # Use only for Image object types
        # (for a photograph, painting, or drawing
        # that represents something else and is
        # considered a museum object, the correct
        # way is to use the ObjectDescription > depicts
        # field).
        # ('image', (
            # ('imageOf', 'image of'),
            # # ('imageIs', 'image is'),
        # )),
    )
    lesser = models.ForeignKey(ObjectRegister, models.CASCADE, related_name='lesser_works')
    greater = models.ForeignKey(ObjectRegister, models.CASCADE, related_name='greater_works')
    relation_type = models.CharField(max_length=31, default='partOf', choices=relation_types)

    def __str__(self):
        return self.lesser.__str__() + ' ' + self.get_relation_type_display + ' ' + self.greater.__str__()

    class Meta:
        unique_together = ('lesser', 'relation_type')

class RelatedObject(models.Model):
    # VRA Core 4
    # The reverse relationships are being tentatively
    # suppressed to keep things systematics, since the
    # database will provide reverse information.
    relation_types = (
        ('default', (
            ('relatedTo', 'related to'),
        ) ),
        ('together', (
            ('designedFor', 'designed for'),
            # ('contextIs', 'context is'),
            ('exhibitedAt', 'exhibited at'), # Not an object-to-object relation
            # ('venueFor', 'venue for'),    # Not an object-to-object relation
            ('mateOf', 'mate of'),
            ('partnerInSetWith', 'partner in set with'),# Not an object-to-object relation
            ('pendantOf', 'pendant of'),
        )),
        ('after', (
            ('depicts', 'depicts'),
            # ('depictedIn', 'depicted in'),
            ('derivedFrom', 'derived from'),
            # ('sourceFor', 'source for'),
        )),
    )
    # Spectrum 4.0 Related object number
    # VRA Core 4   relid
    # Read as 'work1' 'related_association' 'work2'
    work1 = models.ForeignKey('ObjectRegister', models.CASCADE, related_name='relating_work')
    work2 = models.ForeignKey('ObjectRegister', models.CASCADE, related_name='related_work')
    # Spectrum 4.0 Related object association
    # The type of association between the objects (copy, model,
    # representation, etc.)
    relation_type = models.CharField(max_length=31, choices=relation_types, default='relatedTo')
    # Spectrum 4.0 Related object note
    related_note = models.TextField(blank=True)

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
    # Because the TextRef includes a specific citation
    # to the object, it will not be reusable in other
    # objects' records, therefore not Many-to-Many.
    work = models.ForeignKey('ObjectRegister', models.CASCADE)
    # Eventually render the name from a bibliographic
    # database record.
    textref_name = models.CharField(max_length=255)
    textref_name_type = models.CharField(max_length=15, default='book', choices=textref_name_types)
    # If the reference provides a different number for
    # the object, or a citation, record it here:
    textref_refid = models.CharField(max_length=63, blank=True)
    textref_refid_type = models.PositiveSmallIntegerField(default=0, choices=textref_refid_types)
    # Date when the information was located
    textref_datadate = models.DateField(default=timezone.now)
    # Required by SICG:
    textref_location = models.ForeignKey('place.Place', models.PROTECT)
# /VRA Core 4   textref
###########################################################

###########################################################
# Move to a specific application for metadata when project grows:
# Spectrum 4.0 Language
# VRA Core 4   xml:lang
# DCMI         language
class IsoLanguage(models.Model):
    iso = models.CharField(max_length=7, primary_key=True)
    language = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.language
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
