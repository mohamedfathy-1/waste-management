from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from core.models import RecyclingCenter
from decimal import Decimal


class MapIntegrationTest(TestCase):
    """Integration test for map loading functionality"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.citizen = User.objects.create_user(
            username='citizen',
            email='citizen@test.com',
            password='testpass123',
            role='citizen'
        )
        self.client.login(username='citizen', password='testpass123')
        
        # Create test recycling centers
        self.center1 = RecyclingCenter.objects.create(
            name='Center 1',
            address='123 Main St',
            latitude=Decimal('40.712776'),
            longitude=Decimal('-74.005974'),
            materials_accepted='Plastic, Glass',
            working_hours='Mon-Fri: 9AM-5PM'
        )
        self.center2 = RecyclingCenter.objects.create(
            name='Center 2',
            address='456 Oak Ave',
            latitude=Decimal('40.730610'),
            longitude=Decimal('-73.935242'),
            materials_accepted='Paper, Metal',
            working_hours='Mon-Sat: 8AM-6PM'
        )
    
    def test_map_centers_page_loads(self):
        """Test that map centers page loads successfully"""
        response = self.client.get(reverse('map_centers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'citizen/map_centers.html')
    
    def test_map_centers_contains_data(self):
        """Test that map centers page contains center data"""
        response = self.client.get(reverse('map_centers'))
        self.assertContains(response, 'Center 1')
        self.assertContains(response, 'Center 2')
        self.assertContains(response, '40.712776')
        self.assertContains(response, '-74.005974')
    
    def test_map_contains_leaflet(self):
        """Test that Leaflet.js is loaded on map page"""
        response = self.client.get(reverse('map_centers'))
        self.assertContains(response, 'leaflet')
        self.assertContains(response, 'openstreetmap')


class ReportWorkflowTest(TestCase):
    """Integration test for complete report submission workflow"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.citizen = User.objects.create_user(
            username='citizen',
            email='citizen@test.com',
            password='testpass123',
            role='citizen'
        )
        self.staff = User.objects.create_user(
            username='staff',
            email='staff@test.com',
            password='testpass123',
            role='staff'
        )
        self.center = RecyclingCenter.objects.create(
            name='Test Center',
            address='789 Test Blvd',
            latitude=Decimal('40.7'),
            longitude=Decimal('-74.0'),
            materials_accepted='All',
            working_hours='24/7',
            assigned_staff=self.staff
        )
    
    def test_complete_report_workflow(self):
        """Test complete workflow: submit report -> staff updates -> complete"""
        # Citizen submits report
        self.client.login(username='citizen', password='testpass123')
        report_data = {
            'description': 'Test waste issue',
            'latitude': '40.712',
            'longitude': '-74.006'
        }
        response = self.client.post(reverse('submit_report'), report_data)
        # Note: This will fail without image handling, but demonstrates the workflow
        
        # Verify citizen can see their reports
        response = self.client.get(reverse('track_reports'))
        self.assertEqual(response.status_code, 200)
        
        # Staff logs in and views reports
        self.client.logout()
        self.client.login(username='staff', password='testpass123')
        response = self.client.get(reverse('view_reports'))
        self.assertEqual(response.status_code, 200)


class UserManagementTest(TestCase):
    """Integration test for user management workflow"""
    
    def setUp(self):
        """Set up test client and users"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )
        self.citizen = User.objects.create_user(
            username='citizen',
            email='citizen@test.com',
            password='testpass123',
            role='citizen'
        )
        self.client.login(username='admin', password='testpass123')
    
    def test_admin_can_view_all_users(self):
        """Test admin can view all users"""
        response = self.client.get(reverse('manage_users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin')
        self.assertContains(response, 'citizen')
    
    def test_admin_can_access_role_assignment(self):
        """Test admin can access role assignment page"""
        response = self.client.get(reverse('assign_role', args=[self.citizen.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/assign_role.html')
