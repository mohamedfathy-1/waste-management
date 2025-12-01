from django import forms
from .models import WasteReport, RecyclingCenter
from accounts.models import User


class WasteReportForm(forms.ModelForm):
    class Meta:
        model = WasteReport
        fields = ['description', 'latitude', 'longitude', 'image']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the waste issue...'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }


class ReportStatusForm(forms.ModelForm):
    class Meta:
        model = WasteReport
        fields = ['status', 'center']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'center': forms.Select(attrs={'class': 'form-select'}),
        }


class RecyclingCenterForm(forms.ModelForm):
    class Meta:
        model = RecyclingCenter
        fields = ['name', 'address', 'latitude', 'longitude', 'materials_accepted', 'working_hours', 'assigned_staff']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Center Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude', 'step': '0.000001'}),
            'materials_accepted': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g., Plastic, Glass, Paper, Metal'}),
            'working_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mon-Fri: 8AM-5PM, Sat: 9AM-2PM'}),
            'assigned_staff': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show staff users in the assigned_staff dropdown
        self.fields['assigned_staff'].queryset = User.objects.filter(role='staff')
        self.fields['assigned_staff'].required = False


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
        }
