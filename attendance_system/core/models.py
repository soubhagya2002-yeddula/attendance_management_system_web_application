from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES=(
        ('Admin','Admin'),
        ('Manager','Manager'),
        ('Employee','Employee'),
    )

    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='Employee')

    #manager is a foreign key to another user instance

    manager=models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role':'Manager'}
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

class AttendanceRecord(models.Model):
    employee=models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'Employee'})
    date=models.DateField()

    STATUS_CHOICES=(
        ('Present','Present'),
        ('Absent','Absent'),
        ('Leave','Leave'),
    )

    status=models.CharField(max_length=10,choices=STATUS_CHOICES)
    marked_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('employee','date')
        ordering=['date']

    def __str__(self):
        return f"{self.employee.username}-{self.date}:{self.status}"
    
class ApprovalLog(models.Model):
    employee=models.ForeignKey(User,on_delete=models.CASCADE,related_name='attendance_approvals',limit_choices_to={'role':'Employee'})
    manager=models.ForeignKey(User,on_delete=models.CASCADE,related_name='approved_weeks',limit_choices_to={'role':'Manager'})
    week_start_date=models.DateField()
    is_approved=models.BooleanField(default=True)
    approval_signature=models.TextField(blank=True,null=True)
    approved_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('employee','week_start_date')

    def __str__(self):
        return f"Week Starting {self.week_start_date} approved by {self.manager.username} for {self.employee.username}"

