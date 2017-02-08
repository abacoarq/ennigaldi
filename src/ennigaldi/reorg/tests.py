from django.test import TestCase
from .models import *

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
        pass

    def test_generate_refid(self):
        """
        Check that an accession number has been
        generated with the correct fields and values.
        """
        pass
