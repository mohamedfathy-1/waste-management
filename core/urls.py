from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Citizen URLs
    path('citizen/dashboard/', views.citizen_dashboard, name='citizen_dashboard'),
    path('citizen/submit-report/', views.submit_report, name='submit_report'),
    path('citizen/track-reports/', views.track_reports, name='track_reports'),
    path('citizen/map-centers/', views.map_centers, name='map_centers'),
    path('citizen/center/<int:pk>/', views.center_detail, name='center_detail'),
    
    # Staff URLs
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/reports/', views.view_reports, name='view_reports'),
    path('staff/report/<int:pk>/update-status/', views.update_report_status, name='update_report_status'),
    path('staff/center/update/', views.update_center_info, name='update_center_info'),
    
    # Admin URLs
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/reports/', views.manage_reports, name='manage_reports'),
    path('admin-panel/report/<int:pk>/delete/', views.delete_report, name='delete_report'),
    path('admin-panel/centers/', views.manage_centers, name='manage_centers'),
    path('admin-panel/center/add/', views.add_center, name='add_center'),
    path('admin-panel/center/<int:pk>/edit/', views.edit_center, name='edit_center'),
    path('admin-panel/center/<int:pk>/delete/', views.delete_center, name='delete_center'),
    path('admin-panel/users/', views.manage_users, name='manage_users'),
    path('admin-panel/user/<int:pk>/assign-role/', views.assign_role, name='assign_role'),
    path('admin-panel/api/statistics/', views.statistics_api, name='statistics_api'),
]
