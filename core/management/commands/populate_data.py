from django.core.management.base import BaseCommand
from accounts.models import User
from core.models import RecyclingCenter, WasteReport
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create admin user
        admin, created = User.objects.update_or_create(
            username='admin',
            defaults={
                'email': 'admin@wastemanagement.com',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created admin user (username: admin, password: admin123)'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ Updated admin user'))
        
        # Create staff users
        staff_users = [
            {'username': 'staff1', 'email': 'staff1@wastemanagement.com', 'first_name': 'Ahmed', 'last_name': 'Al-Fahad'},
            {'username': 'staff2', 'email': 'staff2@wastemanagement.com', 'first_name': 'Sara', 'last_name': 'Al-Saud'},
        ]
        
        staff_list = []
        for staff_data in staff_users:
            staff, created = User.objects.update_or_create(
                username=staff_data['username'],
                defaults={
                    'email': staff_data['email'],
                    'role': 'staff',
                    'first_name': staff_data['first_name'],
                    'last_name': staff_data['last_name']
                }
            )
            if created:
                staff.set_password('staff123')
                staff.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Created staff user: {staff.username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Updated staff user: {staff.username}'))
            staff_list.append(staff)
        
        # Create citizen users
        citizen_users = [
            {'username': 'citizen1', 'email': 'citizen1@example.com', 'first_name': 'Mohammed', 'last_name': 'Al-Salem'},
            {'username': 'citizen2', 'email': 'citizen2@example.com', 'first_name': 'Fatima', 'last_name': 'Al-Harbi'},
            {'username': 'citizen3', 'email': 'citizen3@example.com', 'first_name': 'Omar', 'last_name': 'Al-Ghamdi'},
        ]
        
        citizen_list = []
        for citizen_data in citizen_users:
            citizen, created = User.objects.update_or_create(
                username=citizen_data['username'],
                defaults={
                    'email': citizen_data['email'],
                    'role': 'citizen',
                    'first_name': citizen_data['first_name'],
                    'last_name': citizen_data['last_name']
                }
            )
            if created:
                citizen.set_password('citizen123')
                citizen.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Created citizen user: {citizen.username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Updated citizen user: {citizen.username}'))
            citizen_list.append(citizen)
        
        # Create recycling centers
        centers_data = [
            {
                'name': 'Riyadh Eco Center',
                'address': 'King Fahd Road, Riyadh, Saudi Arabia',
                'latitude': Decimal('24.7136'),
                'longitude': Decimal('46.6753'),
                'materials_accepted': 'Plastic bottles, Glass containers, Aluminum cans, Paper, Cardboard',
                'working_hours': 'Mon-Fri: 8:00 AM - 5:00 PM, Sat: 9:00 AM - 2:00 PM',
                'assigned_staff': staff_list[0] if staff_list else None
            },
            {
                'name': 'Jeddah Sustainable Waste Hub',
                'address': 'Corniche Road, Jeddah, Saudi Arabia',
                'latitude': Decimal('21.5433'),
                'longitude': Decimal('39.1728'),
                'materials_accepted': 'Electronic waste, Batteries, Metal scraps, Plastic containers',
                'working_hours': 'Mon-Sat: 7:00 AM - 6:00 PM',
                'assigned_staff': staff_list[1] if len(staff_list) > 1 else None
            },
            {
                'name': 'Dammam Community Recycling',
                'address': 'King Abdullah Street, Dammam, Saudi Arabia',
                'latitude': Decimal('26.4207'),
                'longitude': Decimal('50.0888'),
                'materials_accepted': 'Glass, Paper, Cardboard, Organic waste',
                'working_hours': 'Mon-Fri: 9:00 AM - 4:00 PM',
                'assigned_staff': None
            },
        ]
        
        center_list = []
        for center_data in centers_data:
            # Using name as lookup might duplicate if name changed, but here we are changing names.
            # Ideally we'd have a slug or ID. 
            # Since we are "editing" the script, we assume this is the source of truth.
            # If we run this, it will create NEW centers because names are different.
            # That's acceptable for "populate" script usually.
            # To avoid duplicates if run multiple times with SAME names, we use get_or_create.
            center, created = RecyclingCenter.objects.update_or_create(
                name=center_data['name'],
                defaults=center_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created recycling center: {center.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Updated recycling center: {center.name}'))
            center_list.append(center)
        
        # Create waste reports
        # Updating coordinates to be near the new centers
        reports_data = [
            {
                'citizen': citizen_list[0],
                'center': center_list[0],
                'description': 'Large pile of plastic waste near the park entrance. Needs immediate attention.',
                'latitude': Decimal('24.7140'), # Near Riyadh Center
                'longitude': Decimal('46.6760'),
                'status': 'pending'
            },
            {
                'citizen': citizen_list[1],
                'center': center_list[0],
                'description': 'Overflowing trash bins at Main Street shopping center.',
                'latitude': Decimal('24.7150'), # Near Riyadh Center
                'longitude': Decimal('46.6770'),
                'status': 'in_progress'
            },
            {
                'citizen': citizen_list[2],
                'center': center_list[1],
                'description': 'Illegal dumping site with electronic waste and old appliances.',
                'latitude': Decimal('21.5440'), # Near Jeddah Center
                'longitude': Decimal('39.1735'),
                'status': 'pending'
            },
            {
                'citizen': citizen_list[0],
                'center': center_list[1],
                'description': 'Broken glass bottles scattered on sidewalk near school.',
                'latitude': Decimal('21.5450'), # Near Jeddah Center
                'longitude': Decimal('39.1740'),
                'status': 'completed'
            },
            {
                'citizen': citizen_list[1],
                'center': center_list[2],
                'description': 'Cardboard boxes piled up in alley behind restaurants.',
                'latitude': Decimal('26.4215'), # Near Dammam Center
                'longitude': Decimal('50.0895'),
                'status': 'in_progress'
            },
        ]
        
        for report_data in reports_data:
            # Reports are hard to identify uniquely without ID. 
            # We'll just create them if they don't exist exactly matching.
            # Or just leave get_or_create.
            report, created = WasteReport.objects.get_or_create(
                citizen=report_data['citizen'],
                description=report_data['description'],
                defaults=report_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created waste report by {report.citizen.username}'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Creation Complete ==='))
        self.stdout.write('\nLogin Credentials:')
        self.stdout.write(f'  Admin:   username=admin, password=admin123')
        self.stdout.write(f'  Staff:   username=staff1/staff2, password=staff123')
        self.stdout.write(f'  Citizen: username=citizen1/citizen2/citizen3, password=citizen123')
        self.stdout.write(f'\nCreated/Updated {User.objects.count()} users')
        self.stdout.write(f'Created/Updated {RecyclingCenter.objects.count()} recycling centers')
        self.stdout.write(f'Created {WasteReport.objects.count()} waste reports')
