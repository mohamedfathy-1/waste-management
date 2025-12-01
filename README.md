# Waste Management and Recycling System

A comprehensive Django web application for managing waste reports and recycling centers with three distinct user roles: Citizens, Recycling Center Staff, and Administrators.

## Features

### 🔵 Citizen User
- User registration and authentication
- Submit waste reports with image upload and location selection
- Track report status (Pending → In Progress → Completed)
- Interactive map to locate recycling centers
- View recycling center details (materials, hours, address)

### 🟢 Recycling Center Staff
- View reports assigned to their center
- Update report status
- Manage recycling center information
- Track center statistics

### 🔴 Admin User
- Comprehensive dashboard with system statistics
- Manage all waste reports (view, filter, delete)
- Manage recycling centers (CRUD operations)
- Manage users and assign roles
- Advanced filtering and search capabilities

## Technologies Used

- **Backend**: Django 4.2.20
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3
- **Maps**: Leaflet.js 1.9.4 + OpenStreetMap
- **Database**: SQLite
- **Image Handling**: Pillow
- **Python**: 3.11+

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or navigate to the project directory**:
   ```bash
   cd "/Users/macbook/Desktop/Recycle managment system"
   ```

2. **Install required packages**:
   ```bash
   pip3 install django pillow
   ```

3. **Run migrations** (if not already done):
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

4. **Create sample data**:
   ```bash
   python3 manage.py populate_data
   ```

5. **Run the development server**:
   ```bash
   python3 manage.py runserver
   ```

6. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000`

## Login Credentials (Sample Data)

After running `populate_data` command:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Staff | staff1 or staff2 | staff123 |
| Citizen | citizen1, citizen2, or citizen3 | citizen123 |

## Project Structure

```
waste_management_system/
├── manage.py
├── db.sqlite3
├── waste_management_system/      # Project configuration
├── accounts/                      # Authentication app
│   ├── models.py                 # Custom User model
│   ├── views.py                  # Auth views
│   ├── forms.py                  # Registration forms
│   └── decorators.py             # Role-based decorators
├── core/                          # Main application
│   ├── models.py                 # RecyclingCenter, WasteReport
│   ├── views.py                  # All feature views
│   ├── forms.py                  # Application forms
│   └── management/commands/      # Custom management commands
├── templates/                     # HTML templates
│   ├── base.html
│   ├── accounts/
│   ├── citizen/
│   ├── staff/
│   └── admin_panel/
├── static/                        # Static files
│   ├── css/custom.css
│   └── js/main.js
├── media/                         # User uploads
│   └── waste_reports/
├── tests/                         # Test suite
│   ├── test_models.py
│   ├── test_views.py
│   └── test_integration.py
└── documentation/
    └── chapter4.md               # Complete documentation
```

## Key Features Explained

### Role-Based Access Control
The system implements three user roles with distinct permissions:
- **Citizens**: Can submit and track their own waste reports
- **Staff**: Can manage reports assigned to their recycling center
- **Admins**: Have full system access and management capabilities

### Interactive Maps
- **Leaflet.js** integration with OpenStreetMap tiles
- Location selection for waste reports
- All recycling centers displayed on map with markers
- Automatic user location detection
- Nearest center calculation using Haversine formula

### Waste Report Workflow
1. Citizen submits report with description, image, and location
2. System automatically assigns report to nearest recycling center
3. Staff reviews and updates status (Pending → In Progress → Completed)
4. Citizen can track status in real-time

## Running Tests

Run all tests:
```bash
python3 manage.py test
```

Run specific test modules:
```bash
python3 manage.py test tests.test_models
python3 manage.py test tests.test_views
python3 manage.py test tests.test_integration
```

## API Endpoints

### Authentication
- `/accounts/register/` - Citizen registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout

### Citizen Routes
- `/citizen/dashboard/` - Citizen dashboard
- `/citizen/submit-report/` - Submit waste report
- `/citizen/track-reports/` - View all reports
- `/citizen/map-centers/` - Interactive map of centers

### Staff Routes
- `/staff/dashboard/` - Staff dashboard
- `/staff/reports/` - View assigned reports
- `/staff/report/<id>/update-status/` - Update report status
- `/staff/center/update/` - Update center information

### Admin Routes
- `/admin-panel/dashboard/` - Admin dashboard
- `/admin-panel/reports/` - Manage all reports
- `/admin-panel/centers/` - Manage recycling centers
- `/admin-panel/users/` - Manage users and roles

## Documentation

Complete implementation and testing documentation is available in:
`documentation/chapter4.md`

This includes:
- 4.1 Introduction
- 4.2 Technologies Used
- 4.3 System Interfaces
- 4.4 System Coding
- 4.5 System Testing
- 4.6 Deployment Diagram
- 4.7 Conclusion

## Development Tools

### Create Superuser (Alternative to sample data)
```bash
python3 manage.py createsuperuser
```

### Access Django Admin Panel
Navigate to `http://127.0.0.1:8000/admin/`

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` appropriately
- Use environment variables for sensitive data
- Implement HTTPS in production

## License

This project is created for educational purposes.

## Support

For questions or issues, please refer to the documentation in `documentation/chapter4.md`

---

**Made with ❤️ using Django and Bootstrap**
