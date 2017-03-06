from django.db import models
from objectinfo.models import ObjectIdentification, ObjectHierarchy
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import ObjectDoesNotExist
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
    work = models.OneToOneField(ObjectIdentification, models.CASCADE, to_field='work_id', related_name='work_refid', primary_key=True)
    batch = models.ForeignKey(AccessionBatch, models.CASCADE, related_name='batch_works')
    object_number = models.PositiveSmallIntegerField()
    part_number = models.PositiveSmallIntegerField(null=True)
    part_count = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        if self.part_number:
            return self.batch.__str__() + '.' + str(self.object_number) + '-' + str(self.part_number) + '/' + str(self.part_count)
        else:
            return self.batch.__str__() + '.' + str(self.object_number)

    def generate(work_id):
        """
        Generates an AccessionNumber based on active batch,
        previous number, and whether the object is partOf
        another.
        """
        try:
            not AccessionNumber.objects.filter(work=work_id)
        except:
            raise ValueError('Refid already defined for this object!')
        generated = AccessionNumber()
        work = ObjectIdentification.objects.get(pk=work_id)
        generated.work = work

        hasgreater = ObjectHierarchy.objects.filter(relation_type='partOf', lesser=work).exists()
        if hasgreater:
            thegreater = ObjectHierarchy.objects.get(relation_type='partOf', lesser=work)
            try:
                greaternum = AccessionNumber.objects.get(work=thegreater.greater.pk)
            except ObjectDoesNotExist:
                # The line above is not catching the exception, but why?
                raise ObjectDoesNotExist('Parent Object exists, but has no AccessionNumber assigned to it. Generate one on the parent object before attempting to generate on the child.')
        q = AccessionNumber.objects.filter(batch__active=True).last()
        if hasgreater:
            generated.batch = greaternum.batch
            generated.object_number = greaternum.object_number
            p = AccessionNumber.objects.filter(object_number=greaternum.object_number, part_number__gt=0)
            if p:
                n = p.last().part_number
            else:
                n = 0
            generated.part_number = n + 1
            generated.part_count = generated.part_number
            if p:
                p.update(part_count=generated.part_count)
        elif q:
            generated.batch = q.batch
            generated.object_number = q.object_number + 1
        else:
            try:
                generated.batch = AccessionBatch.objects.get(active=True)
            except ObjectDoesNotExist:
                # The line above is not catching the exception, but why?
                raise ObjectDoesNotExist('Please start a batch before attempting to generate an AccessionNumber!')
            generated.object_number = 1
        generated.save()
        # print('Registered accession number ' + generated.__str__() + ' for object ' + work.__str__())

    class Meta:
        index_together=('object_number', 'batch', 'part_number')
        ordering = ['batch', 'object_number', 'part_number']
