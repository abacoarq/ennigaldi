from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from historicdate.models import HistoricDate, DateType
from place.models import Place

###########################################################
# Spectrum 4.0 organisation, people, person
# VRA Core 4   agent
# Dublin Core  contributor, creator, publisher
class Agent(models.Model):
    name_types = (
        ('personal', 'Person'),
        ('corporate', 'Organisation'),
        ('family', 'People'),
        ('other', 'Other'),
    )
    # VRA Core 4   name
    agent_name = models.CharField(max_length=255)
    # Spectrum 4.0 Organisation, people, person
    # VRA Core 4   name > type
    name_type = models.CharField(max_length=15, default='personal', choices=name_types)
    # VRA Core 4   cultura
    # Use controlled vocab, can be replaced by nationality
    # in the case of modern agents.
    agent_culture = models.CharField(max_length=63, blank=True)
    agent_date = models.ManyToManyField(HistoricDate, 'date_for_agent', models.CASCADE, through='AgentDateType')
    # Use this for complex name display or autopopulate from
    # above data using a pre-save hook.
    agent_display = models.CharField(max_length=255)
    # Further identification, if available
    user = models.OneToOneField(User, blank=True)
    orcid = models.CharField(max_length=31, blank=True)
    agent_affiliation = models.ManyToManyField('self', 'employs_agent', models.SET_NULL, through='AgentAffiliation', symmetrical=False)
    # Contact information, if applicable
    email = models.EmailField(blank=True)
    phone_primary = models.CharField(max_length=31, blank=True)
    phone_mobile = models.CharField(max_length=31, blank=True)
    phone_business = models.CharField(max_length=31, blank=True)
    phone_home = models.CharField(max_length=31, blank=True)
    address_1 = models.CharField(max_length=35, blank=True)
    address_2 = models.CharField(max_length=35, blank=True)
    city = models.CharField(max_length=35, blank=True)
    state_province = models.CharField(max_length=31, blank=True)
    zip_code = models.CharField(max_length=31, blank=True)
    # Replace the following field by the Countries Plus list.
    country = models.CharField(max_length=31, blank=True)
    website = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return agent_display

class AgentDateType(DateType):
    date_types = (
        ('life', 'Lived'),
        ('activity', 'Active'),
        ('other', 'Other')
    )
    date_of = models.ForeignKey(Agent, models.CASCADE)

class AgentAffiliation(models.Model):
     agent_person = models.ForeignKey(Agent, models.CASCADE, related_name='employed_in', limit_choices_to={Agent.name_type: 'personal'})
     agent_affiliation = models.ForeignKey(Agent, models.PROTECT, related_name='employs', limit_choices_to=Q(Agent.name_type!='personal'))
     agent_role = models.CharField(max_length=255)
# /Spectrum 4.0 organization, people, person
###########################################################
