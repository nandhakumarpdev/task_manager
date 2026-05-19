from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum, Avg

from .models import Task
from .serializers import TaskSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from datetime import datetime, timedelta



# Create your views here.
# for test only
def hello(request):
    return JsonResponse({"greeting":"hello world"})

# ------------ WorkList --------------------- 
class AllTaskView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get(self, request, user_id):
        queryset = Task.objects.filter(user_id=user_id).order_by('id')
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            reported_time = self.update_report_time(serializer)
            serializer.save(reported_time = reported_time)
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors) 
    
    def update_report_time(self, serializer: TaskSerializer):
        created_at = timezone.now()
        etc = serializer.validated_data["estimate_time_to_complete"]
        time_unit = serializer.validated_data["time_unit"]
        if time_unit == "H":
            reported_time = created_at + timedelta(hours=etc)
        elif time_unit == "D":
             reported_time = created_at + timedelta(days=etc)
        elif time_unit == "W":
            reported_time = created_at + timedelta(weeks=etc)
        else:
            raise ValueError("Invalid time unit")
        return reported_time
    
class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get(self, request, id):
        task = get_object_or_404(Task, pk=id)
        serializer = self.serializer_class(task)
        return Response(serializer.data)
    
    def put(self, request, id):
        task = get_object_or_404(Task, pk=id)
        serializer = self.serializer_class(task, data=request.data, partial=True)
        print("put", serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        task = get_object_or_404(Task, pk=id)
        task.delete()
        return Response({"message": "Task is deleted successfully"})
    
class UserRegistration(APIView):
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response(
                {
                    "error": "All fields required"
                    },
                    staus=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            return Response({"error": "Field already exists"})
        
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        return Response(
            {
                "message" : "User created successfully"
            },
            status=status.HTTP_201_CREATED
        )
    

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Field already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"error": "Email not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(password):
            return Response(
                {"error":"Invalid password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User Login successfully",
                "user_id": user.id, 
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token)
            }
        )
    
class Dashboard(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get(self, request, user_id):
        tasks = Task.objects.filter(user_id=user_id)
        data = {
            "total_tasks": tasks.count(),
            "completed_tasks": tasks.filter(status="D").count(),
            "todo_tasks": tasks.filter(status="T").count(),
            "in_progress_tasks": tasks.filter(status="D").count(),
            "on_hold_tasks": tasks.filter(status="O").count(),
            "low_priority": tasks.filter(priority="L").count(),
            "medium_priority": tasks.filter(priority="M").count(),
            "high_priority": tasks.filter(priority="H").count(),
            "total_average_etc": tasks.aggregate(Avg("estimate_time_to_complete")),
            "total_sum_etc": tasks.aggregate(Sum("estimate_time_to_complete"))
        }
        return Response(data)