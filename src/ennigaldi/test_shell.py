# This is the file for testing individual application functions.
import os
os.environ["LANG"] = "en_US.UTF-8"
import unittest
from django.test import TestCase
from objectinfo.models import ObjectIdentification

class ObjectIdentificationTests(unittest.TestCase):
    def setUp(self):
        ObjectIdentification.objects.create(refid="some_accession_number", source="source of information", description="<p>Description text.</p>", description_source="citation for description", comments="Some comments", distinguishing_features="<p>This object is peculiar because it is a test object.</p>", work_type="Fiddle")
    self.fail('Finish the ObjectIdentification tests.')

class xrefTests(unittest.TestCase):
    # Test every entry that has a foreign key to check
    # if it is referencing properly.
    self.fail('Finish the fkey tests.')

if __name__ == '__main__':
    unittest.main()
