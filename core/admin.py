from django.contrib import admin
from .models import RecyclingCenter, WasteReport


@admin.register(RecyclingCenter)
class RecyclingCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'assigned_staff', 'created_at')
    list_filter = ('created_at', 'assigned_staff')
    search_fields = ('name', 'address', 'materials_accepted')
    raw_id_fields = ('assigned_staff',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'assigned_staff')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Details', {
            'fields': ('materials_accepted', 'working_hours')
        }),
    )


@admin.register(WasteReport)
class WasteReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'citizen', 'center', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'center')
    search_fields = ('citizen__username', 'description')
    raw_id_fields = ('citizen', 'center')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('citizen', 'center', 'status')
        }),
        ('Details', {
            'fields': ('description', 'image')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def has_add_permission(self, request):
        # Only citizens can add reports (through the form, not admin)
        return request.user.is_superuser
