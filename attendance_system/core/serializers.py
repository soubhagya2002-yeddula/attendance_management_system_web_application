from rest_framework import serializers
from .models import AttendanceRecord ,User,ApprovalLog
from datetime import date

class AttendanceMarkSerializer(serializers.ModelSerializer):
    #serializers for marking daily attendance
    class Meta:
        model=AttendanceRecord
        fields=['status']

    def validate(self,data):
        user=self.context['request'].user
        today=date.today()

        if AttendanceRecord.objects.filter(employee=user,date=today).exists():
            raise serializers.ValidationError({"date": "Attendance already marked for today"})
        
        return data

class EmployeeAttendanceSummarySerializer(serializers.ModelSerializer):
    #serializer for viewing personal attendance records

    class Meta:
        model=AttendanceRecord
        fields=['date','status','marked_at']


#manager serializers

class ApprovalLogSerializer(serializers.ModelSerializer):
    #serializer for logging weekly approvals
    employee=serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='Employee'))

    class Meta:
        model=ApprovalLog
        fields=['employee','week_start_date','approval_signature']
        read_only_fields=['manager']