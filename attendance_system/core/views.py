from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .models import AttendanceRecord,User,ApprovalLog
from datetime import date ,timedelta
from django.db.models import Count

# Create your views here.

#----utility functions----

def get_week_range(target_date):
    start_of_week=target_date-timedelta(days=target_date.weekday())
    end_of_week=start_of_week+timedelta(days=6)
    return start_of_week,end_of_week

def role_required(allowed_roles):
    # decorators to check if the user belongs to one of the allowed roles
    from django.contrib.auth.decorators import user_passes_test
    def check_role(user):
        return user.is_authenticated and user.role in allowed_roles
    return user_passes_test(check_role,login_url='/login/')

admin_required=role_required(['Admin'])
manager_required=role_required(['Manager'])
employee_required=role_required(['Employee'])

#Authentication Views

def home_page(request):
    #rendering the landing page
    return render(request, 'core/home.html')

@login_required
def dashboard_view(request):
    #redirects authenticated users to their specific dashboard based on role
    if request.user.role=="Admin":
        return admin_dashboard(request)
    elif request.user.role=='Manager':
        return manager_dashboard(request)
    else:
        return employee_dashboard(request)
    
#--------EMPLOYEE WEB VIEWS=----------

@employee_required
def employee_dashboard(request):
    today=date.today()
    start_of_week,end_of_week=get_week_range(today)

    weekly_attendance=AttendanceRecord.objects.filter(
        employee=request.user,
        date__range=[start_of_week,end_of_week]
    )

    is_approved=ApprovalLog.objects.filter(
        employee=request.user,
        week_start_date=start_of_week
    ).exists()

    context={
        'today':today,
        'weekly_attendance':weekly_attendance,
        'start_of_week':start_of_week,
        'is_approved':is_approved,
        'already_marked_today':AttendanceRecord.objects.filter(employee=request.user,date=today).exists(),

    }
    return render(request,'core/employee_dashboard.html',context)

@employee_required
def mark_attendance(request):
    if request.method=='POST':
        status=request.POST.get('status')
        today=date.today()

        if status in ['Present','Absent','Leave']:
            if not AttendanceRecord.objects.filter(employee=request.user,date=today).exists():
                AttendanceRecord.objects.create(
                  employee=request.user,
                  date=today,
                  status=status
                )
                messages.success(request,f"Attendance Marked as {status}")
            else:
               messages.warning(request,f'Attendance already marked for today')
        else:
            messages.error(request,'Invalid status selected')
    return redirect('dashboard')


#manager web views
@manager_required
def manager_dashboard(request):
    employees=User.objects.filter(manager=request.user,role='Employee').order_by('username')
    today=date.today()
    week_start_date,_=get_week_range(today)

    employee_data=[]
    for emp in employees:
        attendance_counts=AttendanceRecord.objects.filter(
            employee=emp,
            date__range=[week_start_date,week_start_date+timedelta(days=6)]
        ).values('status').annotate(count=Count('status'))

        counts={item['status']:item['count'] for item in attendance_counts}

        approval_log=ApprovalLog.objects.filter(
            employee=emp,
            week_start_date=week_start_date
        ).first()

        employee_data.append({
            'employee':emp,
            'summary':counts,
            'is_approved':bool(approval_log),
            'approval_signature':approval_log.approval_signature if approval_log else '',
            'week_start_date':week_start_date.isoformat()
        })
    context={
        'employee_data':employee_data,
        'current_week_start':week_start_date
    }
    return render(request,'core/manager_dashboard.html',context)

@manager_required
def approve_week(request):
    if request.method=='POST':
        employee_id=request.POST.get('employee_id')
        week_start_date_str=request.POST.get('week_start_date')
        signature=request.POST.get('approval_signature','')

        try:
            employee=User.objects.get(id=employee_id,role='Employee',manager=request.user)
            week_start_date=date.fromisoformat(week_start_date_str)
        except(User.DoesNotExist,ValueError):
            messages.error(request,"invalid employee or date provided")
            return redirect('dashboard')
        
        if not ApprovalLog.objects.filter(employee=employee,week_start_date=week_start_date).exists():
            ApprovalLog.objects.create(
                employee=employee,
                manager=request.user,
                week_start_date=week_start_date,
                approval_signature=signature
            )
            messages.success(request,f"Week approved for {employee.username}")
        else:
            messages.info(request,"week was already approved")
    return redirect('dashboard')

#--------ADMIN WEB VIEWS--------


@admin_required
def admin_dashboard(request):
    all_users=User.objects.all().order_by('role','username')
    context={'all_users':all_users}
    return render(request,'core/admin_dashboard.html',context)

@admin_required
def full_attendance_report(request):
    report_data=AttendanceRecord.objects.select_related('employee').all().order_by('-date','employee_username')
    context={'report_data':report_data}
    return render(request,'core/full_attendance_report.html',context)







