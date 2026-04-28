from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta

# Create your views here.
# for test only
def hello(request):
    return JsonResponse({"greeting":"hello world"})

# ------------ Task handling --------------------- 
class AllTaskView(APIView):
    serializer_class = TaskSerializer
    def get(self, request):
        queryset = Task.objects.all()
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
    serializer_class = TaskSerializer
    def get(self, request, id):
        task = get_object_or_404(Task, pk=id)
        serializer = self.serializer_class(task)
        return Response(serializer.data)
    
    def put(self, request, id):
        task = get_object_or_404(Task, pk=id)
        serializer = self.serializer_class(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        task = get_object_or_404(Task, pk=id)
        task.delete()
        return Response({"message": "Task is deleted successfully"})
    
