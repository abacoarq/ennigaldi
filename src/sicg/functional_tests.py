# This is the file for prototyping application functionality.
# Comments indicate expected user input and application behavior,
# tested by the code.
# First we set up the required imports for Selenium with Chrome on Mac.
import os
os.environ["LANG"] = "en_US.UTF-8"
import unittest
from selenium import webdriver

class entryTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome();

    def tearDown(self):
        self.driver.quit()

    def test_fillEntry(self):
        # User loads home page and finds login prompt
        self.driver.get('http://127.0.0.1:8000/m305')
        assert self.driver.find_element_by_tag_name('form')

        # Prominent button/link to add a new object (A)
        assert self.driver.find_element_by_type('submit')

        # Other links on page: view/edit existing object, (B)
        # add/edit log (future implementation).

        # (A) add new object form

        # First field in form is photo upload;
        # not meant to be a display picture, but rather an ainde-mémoire
        # to let the staff locate the object more easily.

        # Use selector or button to define metadata standard (VRA
        # Core, Spectrum, etc.), which governs how much information
        # will be filled by the user.
        # Possibly later this selector can be moved to a site-wide
        # configuration setting.

        # Agent model is foreign key, allowing new entries to be
        # added on the fly during object entry.
        # Figure out validation scheme for existing agents.

        # Date is also a foreign key model, similar to above.

        # Finish setting up the test later.
        self.fail('Finish the test suite.')

    # Upon saving a new or updated object, the system exports a
    # YAML file with the complete text contents of the entry
    # (and possibly the image filenames?).

    # Should also export an XML file with the VRA Core 4 namespace,
    # if requested (or automatically?)

    # If possible or desired,
    # this exported file ought to be pushed to a specific branch
    # of a git repository. This might help:
    # http://stackoverflow.com/questions/15315573/how-can-i-call-git-pull-from-within-python

    # (B) List view of existing objects is invoked from link on home page.
    # It is displayed as a table or rendered as such by means of div and css.
    # Each line links to the corresponding entry.

    # The list can be reordered according to several criteria, at least:
    # title, agent, accession number.

if __name__ == '__main__':
    unittest.main()
