from django.test import TestCase
from accounts.models import User
from core.models import RecyclingCenter, WasteReport
from decimal import Decimal


class UserModelTest(TestCase):
    """Test cases for the User model"""
    
    def setUp(self):
        """Set up test data"""
        self.citizen = User.objects.create_user(
            username='testcitizen',
            email='citizen@test.com',
            password='testpass123',
            role='citizen'
        )
        self.staff = User.objects.create_user(
            username='teststaff',
            email='staff@test.com',
            password='testpass123',
            role='staff'
        )
        self.admin = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )
    
    def test_user_creation(self):
        """Test that users are created correctly"""
        self.assertEqual(self.citizen.username, 'testcitizen')
        self.assertEqual(self.citizen.role, 'citizen')
        self.assertTrue(self.citizen.check_password('testpass123'))
    
    def test_is_citizen_method(self):
        """Test is_citizen helper method"""
        self.assertTrue(self.citizen.is_citizen())
        self.assertFalse(self.staff.is_citizen())
        self.assertFalse(self.admin.is_citizen())
    
    def test_is_staff_user_method(self):
        """Test is_staff_user helper method"""
        self.assertTrue(self.staff.is_staff_user())
        self.assertFalse(self.citizen.is_staff_user())
        self.assertFalse(self.admin.is_staff_user())
    
    def test_is_admin_user_method(self):
        """Test is_admin_user helper method"""
        self.assertTrue(self.admin.is_admin_user())
        self.assertFalse(self.citizen.is_admin_user())
        self.assertFalse(self.staff.is_admin_user())
    
    def test_user_string_representation(self):
        """Test __str__ method"""
        expected = f"{self.citizen.username} ({self.citizen.get_role_display()})"
        self.assertEqual(str(self.citizen), expected)


class RecyclingCenterModelTest(TestCase):
    """Test cases for the RecyclingCenter model"""
    
    def setUp(self):
        """Set up test data"""
        self.staff = User.objects.create_user(
            username='staffuser',
            email='staff@test.com',
            password='testpass123',
            role='staff'
        )
        self.center = RecyclingCenter.objects.create(
            name='Test Center',
            address='123 Test Street',
            latitude=Decimal('40.712776'),
            longitude=Decimal('-74.005974'),
            materials_accepted='Plastic, Glass, Paper',
            working_hours='Mon-Fri: 8AM-5PM',
            assigned_staff=self.staff
        )
    
    def test_center_creation(self):
        """Test that recycling center is created correctly"""
        self.assertEqual(self.center.name, 'Test Center')
        self.assertEqual(self.center.assigned_staff, self.staff)
    
    def test_center_string_representation(self):
        """Test __str__ method"""
        self.assertEqual(str(self.center), 'Test Center')
    
    def test_center_without_staff(self):
        """Test creating center without assigned staff"""
        center = RecyclingCenter.objects.create(
            name='Unassigned Center',
            address='456 Test Ave',
            latitude=Decimal('40.7'),
            longitude=Decimal('-74.0'),
            materials_accepted='Metal',
            working_hours='24/7'
        )
        self.assertIsNone(center.assigned_staff)


class WasteReportModelTest(TestCase):
    """Test cases for the WasteReport model"""
    
    def setUp(self):
        """Set up test data"""
        self.citizen = User.objects.create_user(
            username='reportcitizen',
            email='citizen@test.com',
            password='testpass123',
            role='citizen'
        )
        self.center = RecyclingCenter.objects.create(
            name='Report Center',
            address='789 Test Blvd',
            latitude=Decimal('40.7'),
            longitude=Decimal('-74.0'),
            materials_accepted='All',
            working_hours='Mon-Fri: 9AM-5PM'
        )
        self.report = WasteReport.objects.create(
            citizen=self.citizen,
            center=self.center,
            description='Test waste report',
            latitude=Decimal('40.712'),
            longitude=Decimal('-74.006'),
            status='pending'
        )
    
    def test_report_creation(self):
        """Test that waste report is created correctly"""
        self.assertEqual(self.report.citizen, self.citizen)
        self.assertEqual(self.report.center, self.center)
        self.assertEqual(self.report.status, 'pending')
    
    def test_report_status_choices(self):
        """Test changing report status"""
        self.report.status = 'in_progress'
        self.report.save()
        self.assertEqual(self.report.status, 'in_progress')
        
        self.report.status = 'completed'
        self.report.save()
        self.assertEqual(self.report.status, 'completed')
    
    def test_report_string_representation(self):
        """Test __str__ method"""
        expected = f"Report by {self.citizen.username} - {self.report.status}"
        self.assertEqual(str(self.report), expected)
    
    def test_report_without_center(self):
        """Test creating report without assigned center"""
        report = WasteReport.objects.create(
            citizen=self.citizen,
            description='Unassigned report',
            latitude=Decimal('40.7'),
            longitude=Decimal('-74.0'),
            status='pending'
        )
        self.assertIsNone(report.center)
    
    def test_report_cascade_delete(self):
        """Test that deleting citizen deletes their reports"""
        report_id = self.report.id
        self.citizen.delete()
        self.assertFalse(WasteReport.objects.filter(id=report_id).exists())
