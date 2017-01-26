from django.db import models
import datetime

class AccessionTable(models.Model):
    year = models.DateField(auto_now_true)
    num = models.PositiveSmallIntegerField(unique_for_year="year")
    retrospective = models.BooleanField(default=False)
