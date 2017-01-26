from django.db import models
import datetime

class AccessionNumber(models.Model):
    accession_number_display = models.CharField(max_length=15)
    year = models.DateField(auto_now_add=True)
    retrospective = models.BooleanField(default=False)
    object_number = models.PositiveSmallIntegerField(unique_for_year="year")
    part_number = models.PositiveSmallIntegerField(blank=True)

    class Meta:
        unique_together=('object_number', 'part_number', 'year')
        ordering = ['-year', '-object_number', 'part_number']
