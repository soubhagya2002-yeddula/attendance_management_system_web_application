from django.urls import path
from . import api_views

urlpatterns=[
    #employee endpoints
    path('employee/mark_attendance/',api_views.MarkAttendanceAPIView.as_view(),name='api_mark_attendance'),
    path('employee/weekly_summary/',api_views.EmployeeWeeklySummaryAPIView.as_view(),name='api_employee_summary'),

    #manager endpoints
    path('manager/approve_week/',api_views.ApproveWeekAPIView.as_view(),name='api_approve_week'),

    #admin endpoints
    
]