from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import ObjectIdentification, ObjectName, ObjectUnit, ObjectHierarchy, IsoLanguage
from storageunit.models import Unit
# from django.urls import resolve
# from objectinfo.views import index

# class homePageTest(django.test.TestCase):
    # def rootResolvesToHome(self):
        # found = resolve('/')
    # self.assertEqual(found.func, index)

# class ObjectIdentificationTests(django.test.TestCase):
    # def setUp(self):
    # self.fail('Finish the ObjectIdentification tests.')

# class xrefTests(unittest.TestCase):
    # # Test every entry that has a foreign key to check
    # # if it is referencing properly.
    # self.fail('Finish the fkey tests.')

class TestObjectIdentification(TestCase):
    def setUp(self):
        # Solution for sample testing image found at:
        # http://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield
        # Image downloaded from placeholder.it
        image = SimpleUploadedFile(name='test_image.jpg', content=open('../sample/350x150.png', 'rb').read(), content_type='image/jpeg')
        ptbr = IsoLanguage.objects.create(iso="pt_BR", language="Portuguese (Brazil)")
        t1 = ObjectName.objects.create(title="Some object", title_type="descriptive", note="Didn't know what to name it", lang=ptbr, source="My own mind", translation="Ceci n'est pas un titre")
        o1 = ObjectIdentification.objects.create(snapshot=image, source="source of information", brief_description="Description text.", description_source="citation for description", comments="Some comments", distinguishing_features="This object is peculiar because it is a test object.", work_type="Fiddle", preferred_title=t1)
        t2 = ObjectName.objects.create(title="Mona Lisa", title_type="creator", note="Uncertain identification of subject", lang=ptbr, source="Wölfflin")
        o2 = ObjectIdentification.objects.create(snapshot=image, source="Vasari", brief_description="Portrait of Lisa del Giocondo", work_type="Painting", preferred_title=t2)
        image.close()

    def test_create_work(self):
        """
        Check that snapshot and name are required
        to save the object.
        """
        o1 = ObjectIdentification.objects.get(brief_description__contains="Description")
        t1 = ObjectName.objects.get(objectidentification__brief_description="Description text.")
        self.assertEqual(t1.objectidentification.comments, "Some comments")
        self.assertEqual(o1.preferred_title.source, "My own mind")

    def test_storage_unit(self):
        o1 = ObjectIdentification.objects.get(brief_description__contains="Description")
        r01f02 = Unit.objects.create(acronym="F02", name="Display case with shelves")
        r01f02a = Unit.objects.create(parent=r01f02, acronym="A", name="Shelf")
        s1 = Unit.objects.get(parent=r01f02)
        stobj = ObjectUnit.objects.create(work=o1, unit=s1, fitness="Inadequate", note="Consider moving elsewhere")

        curstor = o1.storage_unit.last()
        self.assertTrue("Display" in curstor.__str__())

    def test_hierarchy(self):
        o1 = ObjectIdentification.objects.get(preferred_title__translation__contains="Ceci")
        o2 = ObjectIdentification.objects.get(preferred_title__title__contains="Mona")
        p1 = ObjectHierarchy.objects.create(larger=o1, part=o2, relation_type='partOf')

        print(p1)
            # Below not working
        print(o2.has_part.all())
        print(o1.hierarchy.all())
