from django.test import TestCase
from .models import Agent, AgentDateType, AgentAffiliation
from historicdate.models import HistoricDate

class TestAgent(TestCase):
    def setUp(self):
        """
        Attempt the creation of a historic and a modern
        agent, as well as family and corporate agents.
        """
        caesar = Agent.objects.create(name="Gaius Julius Caesar", name_type="personal", culture="Ancient Rome", display="Julius Caesar (Roman, 100–44 B.C.)")
        jane = Agent.objects.create(name="Jane Doe", name_type="personal", display="Jane Doe, Ph.D.", email="janedoe@university.edu")
        uni = Agent.objects.create(name="University of Django", name_type="corporate", display='University of Django, Python', website="www.university.edu")

    def test_agent_fields(self):
        """
        - Check if the objects have been created successfully;
        """
        c = Agent.objects.filter(name__contains="Caesar").first()
        j = Agent.objects.filter(name="Jane Doe").first()
        u = Agent.objects.filter(name_type="corporate").first()

        self.assertEqual(c.name, "Gaius Julius Caesar")
        self.assertEqual(j.email, "janedoe@university.edu")
        self.assertTrue("Python" in u.display)

    def test_agent_dates(self):
        """
        - Check if we can create the proper relationships;
        - Check if the relationships can be queried.
        """
        caesar = Agent.objects.create(name="Gaius Julius Caesar", name_type="personal", culture="Ancient Rome", display="Julius Caesar (Roman, 100–44 B.C.)")
        c_life = HistoricDate.objects.create(display="13 July 100–15 March 44 B.C.", earliest="-100-07-13", earliest_accuracy=False, latest="-44-03-15", latest_accuracy=False)
        c_act = HistoricDate.objects.create(display="60–44 B.C.", earliest="-60", earliest_accuracy=False, latest="-44-03-15", latest_accuracy=False)

        caesar_lives = AgentDateType.objects.create(dated=caesar, datation=c_life, source="Suetonius, Lives of the Caesars", date_type="life")
        caesar_acts = AgentDateType.objects.create(dated=caesar, datation=c_act, source="Livy", date_type="activity")

        self.assertTrue("100" in caesar_lives.datation.earliest)
        self.assertTrue("60" not in caesar_lives.datation.earliest)
        self.assertTrue("60" in caesar_acts.datation.earliest)
        self.assertEqual(caesar,caesar_lives.dated)
