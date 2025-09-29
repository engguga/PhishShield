from django.test import TestCase, Client
from django.urls import reverse
from .models import Campaign, PhishingTemplate, TargetUser, SimulationEvent
import uuid

class ModelTests(TestCase):
    def test_campaign_creation(self):
        campaign = Campaign.objects.create(name="Security Test Campaign")
        self.assertEqual(str(campaign), "Security Test Campaign")
        self.assertTrue(campaign.is_active)

    def test_phishing_template_creation(self):
        template = PhishingTemplate.objects.create(
            name="Test Template",
            subject="Test Subject",
            html_content="<p>Test content</p>"
        )
        self.assertEqual(template.difficulty_level, 2)
        self.assertTrue(template.is_active)

    def test_target_user_creation(self):
        user = TargetUser.objects.create(
            email="test@company.com",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(str(user), "test@company.com")

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = TargetUser.objects.create(
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        self.campaign = Campaign.objects.create(name="Test Campaign")
        self.template = PhishingTemplate.objects.create(
            name="Test Template",
            subject="Test",
            html_content="<p>Test</p>"
        )
        self.simulation = SimulationEvent.objects.create(
            target_user=self.user,
            campaign=self.campaign,
            template=self.template
        )

    def test_track_click_view(self):
        url = reverse('simulations:track_click', args=[self.simulation.unique_simulation_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Refresh to check if clicked was recorded
        self.simulation.refresh_from_db()
        self.assertTrue(self.simulation.clicked_link)

    def test_admin_login_required(self):
        url = reverse('admin:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

class SecurityTests(TestCase):
    def test_simulation_uuid_uniqueness(self):
        user1 = TargetUser.objects.create(email="user1@test.com")
        user2 = TargetUser.objects.create(email="user2@test.com")
        campaign = Campaign.objects.create(name="Test Campaign")
        
        sim1 = SimulationEvent.objects.create(target_user=user1, campaign=campaign)
        sim2 = SimulationEvent.objects.create(target_user=user2, campaign=campaign)
        
        self.assertNotEqual(sim1.unique_simulation_id, sim2.unique_simulation_id)
        self.assertTrue(isinstance(sim1.unique_simulation_id, uuid.UUID))
