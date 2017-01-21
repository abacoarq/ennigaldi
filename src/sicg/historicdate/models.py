from django.db import models
from django.utils import timezone

# Spectrum 4.0 Several fields that use Date or Age
# VRA Core 4   date
# DCMI         Several fields that use a date (created, etc.)
# SICG         Can be used with 2.1 Datação?
# This is the starting point to develop a full-fledged application
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
    work = models.ForeignKey(ObjectIdentification, models.CASCADE)
    description_date = models.ForeignKey(HistoricDate, models.PROTECT)

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
