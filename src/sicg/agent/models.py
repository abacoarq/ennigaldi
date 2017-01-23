from django.db import models
from historicdate import HistoricDate, ObjectDateType

###########################################################
# Spectrum 4.0 organisation, people, person
# VRA Core 4   agent
# Dublin Core  contributor, creator, publisher
class Agent(models.Model):
    # VRA Core 4   name
    agent_name = models.CharField(max_length=255)
    # Spectrum 4.0 Organisation, people, person
    # VRA Core 4   name > type
    name_type = models.CharField(max_length=16, default='personal', choices=name_types)
    # VRA Core 4   cultura
    # Use controlled vocab, can be replaced by nationality
    # in the case of modern agents.
    agent_culture = models.CharField(max_length=64, null=True, blank=True)
    agent_dates = models.ManyToManyField(historicdate.HistoricDate, models.CASCADE, through=AgentDateType, null=True, blank=True)
    agent_display = models.CharField(max_length=255)

    def __str__(self):
        return agent_display

    name_types = (
        ('personal', 'Person'),
        ('corporate', 'Organisation'),
        ('family', 'People'),
        ('other', 'Other')
    )

class AgentDateType(historicdate.AgentDateType):
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
    agent_role = models.CharField(max_length=32)
    # 'False' means the work is securely known, e.g. from a
    # signature, while 'True' means it is attributed.
    attributed = models.BooleanField(default=False)
    attribution_type = models.CharField(max_length=32, null=True, blank=True)
    # Optional field to record complex attribution.
    # If left blank, a pre-save hook should render it from
    # the information provided above.
    agent_role_display = models.CharField(max_length=255)

    def __str__(self):
        return agent_role_display
# /Spectrum 4.0 organization, people, person
###########################################################
