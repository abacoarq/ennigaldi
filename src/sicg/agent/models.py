from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from historicdate import HistoricDate, ObjectDateType
from place import Place
from countries_plus.models import Country

###########################################################
# Spectrum 4.0 organisation, people, person
# VRA Core 4   agent
# Dublin Core  contributor, creator, publisher
class Agent(models.Model):
    # VRA Core 4   name
    agent_name = models.CharField(max_length=255)
    # Spectrum 4.0 Organisation, people, person
    # VRA Core 4   name > type
    name_type = models.CharField(max_length=15, default='personal', choices=name_types)
    # VRA Core 4   cultura
    # Use controlled vocab, can be replaced by nationality
    # in the case of modern agents.
    agent_culture = models.CharField(max_length=63, null=True, blank=True)
    agent_date = models.ManyToManyField(historicdate.HistoricDate, models.CASCADE, through=AgentDateType, null=True, blank=True)
    # Use this for complex name display or autopopulate from
    # above data using a pre-save hook.
    agent_display = models.CharField(max_length=255)
    # Further identification, if available
    user = models.OneToOneField(User, null=True, blank=True)
    orcid = models.CharField(max_length=31, null=True, blank=True)
    agent_affiliation = models.ManyToManyField(Agent, through=AgentAffiliation)
    # Contact information, if applicable
    email = models.EmailField(null=True, blank=True)
    phone_primary = models.CharField(max_length=31, null=True, blank=True)
    phone_mobile = models.CharField(max_length=31, null=True, blank=True)
    phone_business = models.CharField(max_length=31, null=True, blank=True)
    phone_home = models.CharField(max_length=31, null=True, blank=True)
    address_1 = models.CharField(max_length=35, null=True, blank=True)
    address_2 = models.CharField(max_length=35, null=True, blank=True)
    city = models.CharField(max_length=35, null=True, blank=True)
    state_province = models.CharField(max_length=31, null=True, blank=True)
    zip_code = models.CharField(max_length=31, null=True, blank=True)
    # Replace the following field by the Countries Plus list.
    country = models.CharField(max_length=31, null=True, blank=True)
    website = models.CharField(null=True, blank=True)

    def __str__(self):
        return agent_display

    name_types = (
        ('personal', 'Person'),
        ('corporate', 'Organisation'),
        ('family', 'People'),
        ('other', 'Other')
    )

class AgentDateType(historicdate.DateType):
    date_of = models.ForeignKey(Agent, models.CASCADE)

    date_types = (
        ('life', 'Lived'),
        ('activity', 'Active'),
        ('other', 'Other')
    )

class AgentRole(models.Model):
    agent = models.ForeignKey(Agent, models.PROTECT)
    work = models.ForeignKey(objectinfo.ObjectIdentification, models.PROTECT)
    # VRA Core 4 agent > role
    # Use controlled vocab
    agent_role = models.CharField(max_length=31)
    # 'False' means the work is securely known, e.g. from a
    # signature, while 'True' means it is attributed.
    attributed = models.BooleanField(default=False)
    attribution_type = models.CharField(max_length=31, null=True, blank=True)
    # Optional field to record complex attribution.
    # If left blank, a pre-save hook should render it from
    # the information provided above.
    agent_role_display = models.CharField(max_length=255)

    def __str__(self):
        return agent_role_display

class AgentAffiliation(models.Model):
    agent_person = models.ForeignKey(Agent, limit_choices_to={name_type: 'personal'})
    agent_affiliation = models.ForeignKey(Agent, limit_choices_to=Q(name_type!='personal'))
    agent_role = models.CharField(max_length=255)
# /Spectrum 4.0 organization, people, person
###########################################################
