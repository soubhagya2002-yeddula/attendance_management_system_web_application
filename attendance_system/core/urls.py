from django.urls import path
from django.contrib.auth import  views as auth_views
from . import views

urlpatterns = [
    #homepage and auth

    path('',views.home_page,name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='core/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),

    #dashboard router
    path('dashboard/',views.dashboard_view,name='dashboard'),

    #employee web routes
    path('employee/mark_attendance/',views.mark_attendance,name='mark_attendance'),

    #manager web routes
    path('manager/approve_week/',views.approve_week,name='approve_week'),

    #admin web routes
    path('admin/report/',views.full_attendance_report,name='full_report'),

]
