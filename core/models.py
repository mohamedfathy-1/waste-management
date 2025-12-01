from django.db import models
from django.conf import settings


class RecyclingCenter(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    materials_accepted = models.TextField(help_text="Comma-separated list of materials accepted")
    working_hours = models.CharField(max_length=200, help_text="e.g., Mon-Fri: 8AM-5PM")
    assigned_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'role': 'staff'},
        related_name='assigned_center'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Recycling Center'
        verbose_name_plural = 'Recycling Centers'
        ordering = ['name']


class WasteReport(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    
    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='waste_reports',
        limit_choices_to={'role': 'citizen'}
    )
    center = models.ForeignKey(
        RecyclingCenter, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reports'
    )
    image = models.ImageField(upload_to='waste_reports/', blank=True, null=True)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Report by {self.citizen.username} - {self.status}"
    
    class Meta:
        verbose_name = 'Waste Report'
        verbose_name_plural = 'Waste Reports'
        ordering = ['-created_at']
