from django.db import models

# Spectrum 4.0 Several fields that use Date or Age
# VRA Core 4   date
# DCMI         Several fields that use a date (created, etc.)
# SICG         Can be used with 2.1 Datação?
# This is the starting point to develop a full-fledged application
# to produce timelines and comparisons: see theoretical model at
# http://www.museumsandtheweb.com/biblio/issues_in_historical_geography.html
class HistoricDate(models.Model):
    # VRA Core 4   only allows a True/False setting for 'circa'
    # Not provided in other standards.
    date_accuracy = (
        (0, ''),
        (1, 'before'),
        (2, 'up to'),
        (3, 'circa'),
        (4, 'from'),
        (5, 'after'),
    )
    # Defined by the VRA Core 4 restricted XML schema.
    # The date model attempts to follow ISO-8601 with accommodations
    # for historic requirements, so the format must be filled
    # with the relevant choice of information from the example below:
    # [+ or -][year]-[month]-[day]
    #
    # For example:
    # 13 billion years ago: -13000000000
    # Ides of March, 44 B.C.: -44-03-15
    # January, 1792: 1792-01
    #
    # An example of a complex date:
    # 'First half of the 5th century B.C.'
    # -425, date_accuracy=3
    #
    date_earliest = models.CharField(max_length=15)
    date_earliest_accuracy = models.PositiveSmallIntegerField(max_length=1, choices=date_accuracy, default=0)
    # Enter 'present' if living person or continued event.
    date_latest = models.CharField(max_length=15)
    date_latest_accuracy = models.PositiveSmallIntegerField(max_length=1, choices=date_accuracy, default=0)
    date_source = models.CharField(max_length=255, blank=True)
    # Text representation of the date, for when more complex
    # explanations are required. If left blank, will be filled
    # with rendered concatenation of the previous fields
    # at a pre-save hook.
    date_display = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return date_display

# VRA Core 4   date > type
# In VRA Core, 'date' is an attribute of any of the
# three root-level classes (work, agent, or image),
# and has distinct allowed date types accordingly.
# All other standards use a specific field for each date type,
# e.g. Spectrum 4.0 Production date, DCMI created, issued, etc.
# This model is not to be used directly, but subclassed to fit
# the requirements of the requesting object.
class DateType(models.Model):
    date_types = (
        ('alteration', 'Altered'),
        ('broadcast', 'Broadcast'),
        ('bulk', 'Bulk'),
        ('commission', 'Commissioned'),
        ('creation', 'Created'),
        ('design', 'Designed'),
        ('destruction', 'Destroyed or demolished'),
        ('discovery', 'Discovered'),
        ('exhibition', 'Exhibited'),
        ('inclusive', 'Inclusive'),
        ('performance', 'Performed'),
        ('publication', 'Published'),
        ('restoration', 'Restored'),
        ('view', 'Viewed'),
        ('other', 'Other')
    )
    # Date types in VRA Core are the types of events defined
    # by that date, e.g. creation, discovery, removal, etc.
    date_type = models.CharField(max_length=31, choices=date_types)
    # VRA Core 4   date > source
    # Turn into fkey to bibliographic record
    date_source = models.CharField(max_length=255, null=True, blank=True)
    date_of = models.ForeignKey('genericmodel', models.CASCADE)
    date_value = models.ForeignKey(HistoricDate, models.PROTECT)
