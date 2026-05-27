from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, UserDetails

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = "__all__"
