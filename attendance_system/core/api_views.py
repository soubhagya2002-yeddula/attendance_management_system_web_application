from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import AttendanceRecord,User
from .serializers import AttendanceMarkSerializer,EmployeeAttendanceSummarySerializer,ApprovalLogSerializer
from datetime import date,timedelta
#utility function from views.py
from .views import get_week_range 

#CUSTOM PERMISSION CLASSES (role based access control for api)

class IsEmployee(IsAuthenticated):
    def has_permission(self,request,view):
        return super().has_permission(request,view) and request.user.role=='Employee'
    
class IsManager(IsAuthenticated):
    def has_permission(self,request,view):
        return super().has_permission(request,view) and request.user.role=='Manager'
    

#---------------employee api views------------------

class MarkAttendanceAPIView(APIView):
    permission_classes=[IsEmployee]

    def post(self,request):
        serializer=AttendanceMarkSerializer(data=request.data,context={'request':request})

        if serializer.is_valid():
            serializer.save(employee=request.user,date=date.today())
            return Response({"message":"Attendance marked successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class EmployeeWeeklySummaryAPIView(APIView):
    permission_classes=[IsEmployee]

    def get(self,request):
        today=date.today()
        start_of_week,end_of_week=get_week_range(today)

        weekly_records=AttendanceRecord.objects.filter(
            employee=request.user,
            date__range=[start_of_week,end_of_week]
        )

        serializer=EmployeeAttendanceSummarySerializer(weekly_records,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

#-----MANAGER API VIEWS-----------------

class ApproveWeekAPIView(APIView):
    permission_classes=[IsManager]

    def post(self,request):
        serializer=ApprovalLogSerializer(data=request.data,context={'request':request})

        if serializer.is_valid():
            employee_instance=serializer.validated_data.get('employee')
            week_start_date=serializer.validated_data.get('week_start_date')

            #ensure employee reports to the current manager
            if employee_instance.manager!=request.user:
                return Response({"detail":"you do not manage this employee"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


