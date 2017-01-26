from django.test import TestCase
from django.core.urlresolvers import resolve
from objectinfo.views import index

class homePageTest(django.test.TestCase):
    def rootResolvesToHome(self):
        found = resolve('/')
    self.assertEqual(found.func, index)

class ObjectIdentificationTests(django.test.TestCase):
    def setUp(self):
        ObjectIdentification.objects.create(refid="some_accession_number", source="source of information", description="<p>Description text.</p>", description_source="citation for description", comments="Some comments", distinguishing_features="<p>This object is peculiar because it is a test object.</p>", work_type="Fiddle")
    self.fail('Finish the ObjectIdentification tests.')

class xrefTests(unittest.TestCase):
    # Test every entry that has a foreign key to check
    # if it is referencing properly.
    self.fail('Finish the fkey tests.')
