from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import *
from objectinfo.models import ObjectRegister, Hierarchy, ObjectName, IsoLanguage

class TestStartBatch(TestCase):
    def setUp(self):
        AccessionBatch.start_batch(retrospective=True, batch_note="Retrospective")
        AccessionBatch.start_batch(retrospective=False, batch_note="Non retrospective")

    def test_batch_fields(self):
        """
        Check if all fields have been automatically filled
        with the correct defaults.
        """
        retro = AccessionBatch.objects.filter(retrospective=True).first()
        non_retro = AccessionBatch.objects.filter(retrospective=False).first()
        self.assertEqual(retro.__str__(), '2017.R.1')
        self.assertEqual(non_retro.__str__(), '2017.2')
        self.assertEqual(retro.active, False)
        self.assertEqual(non_retro.active, True)

class TestGenerateRefid(TestCase):
    def setUp(self):
        AccessionBatch.start_batch(retrospective=True, batch_note="Retrospective")
        image = SimpleUploadedFile(name='test_image.jpg', content=open('../sample/350x150.png', 'rb').read(), content_type='image/jpeg')
        ptbr = IsoLanguage.objects.create(iso="pt_BR", language="Portuguese (Brazil)")
        t1 = ObjectName.objects.create(title="Some object", title_type="descriptive", note="Didn't know what to name it", lang=ptbr, source="My own mind", translation="Ceci n'est pas un titre")
        o1 = ObjectRegister.objects.create(snapshot=image, source="source of information", brief_description="Description text.", description_source="citation for description", comments="Some comments", distinguishing_features="This object is peculiar because it is a test object.", work_type="Fiddle", preferred_title=t1)
        t2 = ObjectName.objects.create(title="Mona Lisa", title_type="creator", note="Uncertain identification of subject", lang=ptbr, source="Wölfflin")
        o2 = ObjectRegister.objects.create(snapshot=image, source="Vasari", brief_description="Portrait of Lisa Gherardini", work_type="Painting", preferred_title=t2)
        t3 = ObjectName.objects.create(title="Thinker", title_type="creator", note="also allegory for empty thoughts", lang=ptbr, source="Rodin himself")
        o3 = ObjectRegister.objects.create(snapshot=image, source="source of information for object 3", brief_description="Description text for object 3.", description_source="citation for description 3", comments="Some comments on object 3", distinguishing_features="This object is designed to test accession numbering.", work_type="Test", preferred_title=t3)
        p1 = Hierarchy.objects.create(lesser=o1, greater=o2, relation_type='partOf')
        p2 = Hierarchy.objects.create(lesser=o3, greater=o2, relation_type='partOf')
        image.close()

    def test_generate_refid(self):
        """
        Check that an accession number has been
        generated with the correct fields and values.
        """
        o1 = ObjectRegister.objects.get(preferred_title__translation__contains="Ceci")
        o2 = ObjectRegister.objects.get(preferred_title__title__contains="Mona")
        o3 = ObjectRegister.objects.get(preferred_title__title__contains="Think")
        n2 = AccessionNumber.generate(o2.pk)
        n1 = AccessionNumber.generate(o1.pk)
        n3 = AccessionNumber.generate(o3.pk)
        num2 = AccessionNumber.objects.get(pk=o2.pk)
        num1 = AccessionNumber.objects.get(pk=o1.pk)
        self.assertEqual(num1.part_count,2)
