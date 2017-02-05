from django.db import models
import datetime

class AccessionNumber(models.Model):
    accession_number_display = models.CharField(max_length=15, unique=True)
    year = models.DateField(auto_now_add=True)
    retrospective = models.BooleanField(default=True, help_text="Select this if the object is not being recorded in the same year it entered the organisation.")
    object_number = models.PositiveIntegerField(unique_for_year="year")
    part_number = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        return accession_number_display

    class Meta:
        index_together=('object_number', 'part_number', 'year')
        ordering = ['-year', '-object_number', 'part_number']
