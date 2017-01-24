from django.test import TestCase
from django.core.urlresolvers import resolve
from objectinfo.views import index

class homePageTest(TestCase):
    def rootResolvesToHome(self):
        found = resolve('/')
        self.assertEqual(found.func, index)
