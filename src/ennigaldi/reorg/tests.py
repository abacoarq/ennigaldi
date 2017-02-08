from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import *
from objectinfo.models import ObjectIdentification, ObjectHierarchy, ObjectName, IsoLanguage

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

def TestGenerateRefid(TestCase):
    def setUp(self):
        AccessionBatch.start_batch(retrospective=True, batch_note="Retrospective")
        ptbr = IsoLanguage.objects.create(iso="pt_BR", language="Portuguese (Brazil)")
        t1 = ObjectName.objects.create(title="Some object", title_type="descriptive", note="Didn't know what to name it", lang=ptbr, source="My own mind", translation="Ceci n'est pas un titre")
        o1 = ObjectIdentification.objects.create(snapshot=image, source="source of information", brief_description="Description text.", description_source="citation for description", comments="Some comments", distinguishing_features="This object is peculiar because it is a test object.", work_type="Fiddle", preferred_title=t1)
        t2 = ObjectName.objects.create(title="Mona Lisa", title_type="creator", note="Uncertain identification of subject", lang=ptbr, source="Wölfflin")
        o2 = ObjectIdentification.objects.create(snapshot=image, source="Vasari", brief_description="Portrait of Lisa Gherardini", work_type="Painting", preferred_title=t2)
        p1 = ObjectHierarchy.objects.create(lesser=o1, greater=o2, relation_type='partOf')
        image.close()
        n1 = AccessionNumber.generate()
        n2 = AccessionNumber.generate()

    def test_generate_refid(self):
        """
        Check that an accession number has been
        generated with the correct fields and values.
        """
        pass
