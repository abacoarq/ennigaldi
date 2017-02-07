from django.test import TestCase
from .models import Unit

class TestStorageUnit(TestCase):
    def setUp(self):
        bldg = Unit.objects.create(acronym='B00', name="Main Building", note="The one and only museum building we have here.")
        r01 = Unit.objects.create(parent=bldg, acronym="R01", name="Greek archaeology gallery")
        r02 = Unit.objects.create(parent=bldg, acronym="R02", name="Medieval sculpture gallery", note="To be emptied for renovation soon.")
        r01f01 = Unit.objects.create(parent=r01, acronym="F01", name="Simple display case with glass dome")
        r01f02 = Unit.objects.create(parent=r01, acronym="F02", name="Display case with shelves")
        r01f02a = Unit.objects.create(parent=r01f02, acronym="A", name="Shelf")

    def test_unit_strings(self):
        """
        Make sure all parts of the string are present as expected.
        """
        bldg = Unit.objects.get(name="Main Building")
        r02 = Unit.objects.get(name__contains="Medieval")
        r01f01 = Unit.objects.get(acronym="F01")
        r01f02a = Unit.objects.get(name="Shelf")

        self.assertEqual(bldg.__str__(), "B00 Main Building")
        self.assertTrue("Main Building" in r02.__str__())
        self.assertTrue("Main Building" in r01f01.__str__())
        self.assertTrue("Greek" in r01f01.__str__())
        self.assertTrue("A" in r01f02a.__str__())
