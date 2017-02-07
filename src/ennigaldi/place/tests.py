from django.test import TestCase
from .models import Place

class PlaceTest(TestCase):
    def setUp(self):
        Place.objects.create(location_name="Rome", location_name_type="geographic", location_extent="Ancient city of Rome", city="Rome", state_province="Italy", country="Roman Empire")
        Place.objects.create(location_name="Utopia National Museum", location_name_type="corporate", email="museum@utopia.ut", phone_primary="+99 555-6789", website="www.utopiamuseum.gov.ut", address_1="34 Neverland Street", city="Amaurot", country="Utopia")

    def test_place_fields(self):
        r = Place.objects.filter(location_name="Rome", location_extent="Ancient city of Rome").first()
        u = Place.objects.filter(location_name="Utopia National Museum").first()
        self.assertEqual(r.country, "Roman Empire")
        self.assertEqual(u.city, "Amaurot")
        self.assertEqual(r.__str__(), "Rome (Ancient city of Rome)")
        self.assertEqual(u.__str__(), "Utopia National Museum (Amaurot)")
