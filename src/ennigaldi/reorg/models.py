from django.db import models
from objectinfo.models import ObjectIdentification, ObjectHierarchy
from django.contrib.auth.models import User
from datetime import datetime as dt

class AccessionBatch(models.Model):
    batch_datadate = models.DateField(auto_now_add=True)
    batch_year = models.PositiveSmallIntegerField()
    batch_number = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=True)
    batch_note = models.TextField(blank=True)
    retrospective = models.BooleanField(default=False)

    def start_batch(retrospective, batch_note):
        AccessionBatch.objects.all().update(active=False)
        b = AccessionBatch()
        b.batch_year = dt.now().year
        last_batch = AccessionBatch.objects.filter(batch_year=dt.now().year).first()
        if last_batch:
            last_batch_num = last_batch.batch_number
            b.batch_number = last_batch_num + 1
        else:
            b.batch_number = 1
        b.retrospective=True if retrospective else False
        b.active = True
        b.save()
        big_r = '.R.' if b.retrospective else '.'
        return 'Working on batch ' + str(b.batch_year) + big_r + str(b.batch_number) + ' since ' + b.batch_datadate.strftime('%Y-%m-%d')

    def __str__(self):
        big_r = '.R.' if self.retrospective else '.'
        return str(self.batch_year) + big_r + str(self.batch_number)

    class Meta:
        ordering = ['-batch_year', '-batch_number']
        index_together = ('batch_year', 'batch_number')

class AccessionNumber(models.Model):
    work = models.OneToOneField(ObjectIdentification, models.CASCADE, to_field='work_id', related_name='refid', primary_key=True)
    accession_batch = models.ForeignKey(AccessionBatch, models.CASCADE, related_name='batch_works')
    object_number = models.PositiveIntegerField()
    part_number = models.PositiveSmallIntegerField(blank=True)
    part_count = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        if part_number:
            return accession_batch + '.' + object_number + '-' + part_number + '/' + part_count
        else:
            return accession_batch + '.' + object_number

    def generate(self):
        p = ObjectIdentification.is_part()
        q = AccessionNumber.objects.filter(accession_batch__active=True)
        if AccessionNumber.objects.get(pk=self.work):
            raise ValueError('Refid already defined for this object!')
        # To generate the object and part numbers:
        # 1. If the object is a part, get the parent
        # object number, look up existing parts and
        # increment part_number by 1.
        if p:
            current_set = AccessionNumber.objects.filter(accession_batch=self.accession_batch, object_number=self.object_number)
            self.object_number = AccessionNumber.objects.get(pk=p).object_number
            self.accession_batch = AccessionBatch.objects.get(accessionnumber__work=p)
            self.part_number = current_set.last().part_number + 1
            self.part_count = self.part_number
            current_set.update(part_count=self.part_number)
        # 2. If the object is not a part,
        # look up the most recent object number from
        # the current batch and increment by 1.
        elif q:
            object_number = q.last().object_number + 1
        else:
            object_number = 1
        self.save()
        return 'Registered accession number ' + __str__(self)

    class Meta:
        index_together=('object_number', 'accession_batch', 'part_number')
        ordering = ['accession_batch', 'object_number', 'part_number']
