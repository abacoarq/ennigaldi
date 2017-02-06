from django.db import models
import datetime

class AccessionNumber(models.Model):
    accession_number_display = models.CharField(max_length=15, unique=True)
    accessed_year = models.PositiveSmallIntegerField()
    retrospective = models.BooleanField(default=True, help_text="Select this if the object is not being recorded in the same year it entered the organisation.")
    object_number = models.PositiveIntegerField(unique_for_year="accessed_year")
    part_number = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        return accession_number_display

    def autofill(self):
        self.accessed_year = now.year
        # To generate the object and part numbers:
        # 1. If the object is a part, get the parent
        # object number, look up existing parts
        # 2. If the object is not a part,
        # look up the most recent object number from
        # the current year.
        self.save()

    class Meta:
        index_together=('object_number', 'part_number', 'accessed_year')
        ordering = ['-accessed_year', '-object_number', 'part_number']
