from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='citizen')
    email = models.EmailField(unique=True)
    
    def is_citizen(self):
        return self.role == 'citizen'
    
    def is_staff_user(self):
        return self.role == 'staff'
    
    def is_admin_user(self):
        return self.role == 'admin'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
