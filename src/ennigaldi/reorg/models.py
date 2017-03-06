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
    batch = models.ForeignKey(AccessionBatch, models.CASCADE, related_name='batch_works')
    object_number = models.PositiveSmallIntegerField()
    part_number = models.PositiveSmallIntegerField(null=True)
    part_count = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        if part_number:
            return batch + '.' + object_number + '-' + part_number + '/' + part_count
        else:
            return batch + '.' + object_number

    def generate(self, work):
        """
        Generates an AccessionNumber based on active batch,
        previous number, and whether the object is a partOf
        another.
        """
        # if AccessionNumber.objects.get(pk=work):
            # raise ValueError('Refid already defined for this object!')
        g = ObjectHierarchy.objects.get(relation_type='partOf', lesser=work).greater
        h = AccessionNumber.objects.filter(work=g).first()
        q = AccessionNumber.objects.filter(batch__active=True).last()
        self.work = work
        if h:
            self.batch = h.batch
            self.object_number = h.object_number
            p = AccessionNumber.objects.filter(object_number=h.object_number, part_number__gt=0)
            if p:
                n = p.last().part_number
            else:
                n = 0
            self.part_number = n + 1
            self.part_count = self.part_number
            if p:
                p.update(part_count=self.part_count)
        elif g:
            raise NameError('Parent object exists, but has no AccessionNumber assigned to it. Generate one on the parent object before attempting to generate on the child.')
        elif q:
            self.batch = q.batch
            self.object_number = q.object_number + 1
        else:
            try:
                self.batch = AccessionBatch.objects.get(active=True)
            except:
                raise NameError('Please start a batch before attempting to generate an AccessionNumber!')
            self.object_number = 1
        self.save()
        print('Registered accession number ' + self.__str__() + ' for object ' + work.__str__())

    class Meta:
        index_together=('object_number', 'batch', 'part_number')
        ordering = ['batch', 'object_number', 'part_number']
