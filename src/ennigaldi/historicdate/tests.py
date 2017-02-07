from django.test import TestCase
from .models import *

class HistoricDateTest(TestCase):
    def setUp(self):
        HistoricDate.objects.create(display="Há dez mil anos atrás", earliest="-11000", earliest_accuracy=True, latest="-9000", latest_accuracy=True)
        HistoricDate.objects.create(display="Ides of March, 44 B.C.", earliest="-44-03-15", earliest_accuracy=False)

    def test_historicdate_fields(self):
        """
        Check if dates are created correctly
        """
        raul = HistoricDate.objects.filter(earliest="-11000").first()
        caesar = HistoricDate.objects.filter(earliest="-44-03-15").first()
        self.assertEqual(raul.__str__(), "Há dez mil anos atrás")
        self.assertEqual(raul.latest_accuracy, True)
        self.assertEqual(caesar.earliest, "-44-03-15")
        self.assertEqual(caesar.earliest_accuracy, False)
