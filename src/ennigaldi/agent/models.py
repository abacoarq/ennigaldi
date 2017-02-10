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
    name = models.CharField(max_length=255)
    # Spectrum 4.0 Organisation, people, person
    # VRA Core 4   name > type
    name_type = models.CharField(max_length=15, default='personal', choices=name_types)
    # VRA Core 4   cultura
    # Use controlled vocab, can be replaced by nationality
    # in the case of modern agents.
    culture = models.CharField(max_length=63, blank=True)
    dates = models.ManyToManyField(HistoricDate, related_name='date_for_agent', through='AgentDateType')
    # Use this for complex name display or autopopulate from
    # above data using a pre-save hook.
    display = models.CharField(max_length=255)
    # Further identification, if available
    user = models.OneToOneField(User, models.CASCADE, null=True)
    orcid = models.CharField(max_length=31, blank=True)
    affiliation = models.ManyToManyField('self', related_name='employs', through='AgentAffiliation', symmetrical=False)
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
        return self.display

class AgentDateType(DateType):
    date_types = (
        ('life', 'Lived'),
        ('activity', 'Active'),
        ('other', 'Other')
    )

    dated = models.ForeignKey(Agent, models.CASCADE)
    date_type = models.CharField(max_length=31, choices=date_types)

    def __str__(self):
        return self.dated.name + ' (' + self.get_date_type_display + ' ' + self.datation.display + ')'

class AgentAffiliation(models.Model):
    person = models.ForeignKey(Agent, models.CASCADE, related_name='employee', limit_choices_to={Agent.name_type: 'personal'})
    organisation = models.ForeignKey(Agent, models.PROTECT, related_name='employer', limit_choices_to=Q(Agent.name_type!='personal'))
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.person.__str__() + ' is ' + self.role + ' at ' + self.organisation.__str__()
# /Spectrum 4.0 organization, people, person
###########################################################
