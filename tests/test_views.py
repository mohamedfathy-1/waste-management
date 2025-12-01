from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from core.models import RecyclingCenter, WasteReport
from decimal import Decimal


class AuthenticationViewTest(TestCase):
    """Test cases for authentication views"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='citizen'
        )
    
    def test_register_view_get(self):
        """Test registration page loads"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
    
    def test_register_view_post(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)
    
    def test_login_view_get(self):
        """Test login page loads"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_login_view_post_success(self):
        """Test successful login"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login


class CitizenViewTest(TestCase):
    """Test cases for citizen views"""
    
    def setUp(self):
        """Set up test client and citizen user"""
        self.client = Client()
        self.citizen = User.objects.create_user(
            username='citizen',
            email='citizen@test.com',
            password='testpass123',
            role='citizen'
        )
        self.client.login(username='citizen', password='testpass123')
    
    def test_citizen_dashboard_access(self):
        """Test citizen can access dashboard"""
        response = self.client.get(reverse('citizen_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'citizen/dashboard.html')
    
    def test_submit_report_view(self):
        """Test submit report page loads"""
        response = self.client.get(reverse('submit_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'citizen/submit_report.html')
    
    def test_track_reports_view(self):
        """Test track reports page loads"""
        response = self.client.get(reverse('track_reports'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'citizen/track_reports.html')
    
    def test_map_centers_view(self):
        """Test map centers page loads"""
        response = self.client.get(reverse('map_centers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'citizen/map_centers.html')


class StaffViewTest(TestCase):
    """Test cases for staff views"""
    
    def setUp(self):
        """Set up test client and staff user"""
        self.client = Client()
        self.staff = User.objects.create_user(
            username='staff',
            email='staff@test.com',
            password='testpass123',
            role='staff'
        )
        self.center = RecyclingCenter.objects.create(
            name='Test Center',
            address='123 Test St',
            latitude=Decimal('40.7'),
            longitude=Decimal('-74.0'),
            materials_accepted='All',
            working_hours='Mon-Fri: 9AM-5PM',
            assigned_staff=self.staff
        )
        self.client.login(username='staff', password='testpass123')
    
    def test_staff_dashboard_access(self):
        """Test staff can access dashboard"""
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/dashboard.html')
    
    def test_view_reports_access(self):
        """Test staff can view reports"""
        response = self.client.get(reverse('view_reports'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/view_reports.html')


class AdminViewTest(TestCase):
    """Test cases for admin views"""
    
    def setUp(self):
        """Set up test client and admin user"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )
        self.client.login(username='admin', password='testpass123')
    
    def test_admin_dashboard_access(self):
        """Test admin can access dashboard"""
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/dashboard.html')
    
    def test_manage_reports_access(self):
        """Test admin can access manage reports"""
        response = self.client.get(reverse('manage_reports'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/manage_reports.html')
    
    def test_manage_centers_access(self):
        """Test admin can access manage centers"""
        response = self.client.get(reverse('manage_centers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/manage_centers.html')
    
    def test_manage_users_access(self):
        """Test admin can access manage users"""
        response = self.client.get(reverse('manage_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/manage_users.html')


class PermissionTest(TestCase):
    """Test cases for role-based permissions"""
    
    def setUp(self):
        """Set up test users"""
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
    
    def test_citizen_cannot_access_admin_dashboard(self):
        """Test citizen cannot access admin dashboard"""
        self.client.login(username='citizen', password='testpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertNotEqual(response.status_code, 200)
    
    def test_staff_cannot_access_admin_dashboard(self):
        """Test staff cannot access admin dashboard"""
        self.client.login(username='staff', password='testpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertNotEqual(response.status_code, 200)
    
    def test_unauthenticated_redirect(self):
        """Test unauthenticated users are redirected"""
        response = self.client.get(reverse('citizen_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
