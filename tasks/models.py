from django.db import models
from django.contrib.auth.models import User

# ------Task models-----------
class Priority(models.TextChoices):
    LOW = "L"
    MEDIUM = "M"
    HIGH = "H"

class TimeUnit(models.TextChoices):
    HOUR = "H"
    DAY = "D"
    WEEK = "W"

class TaskStatus(models.TextChoices):
    TODO = "T"    
    IN_PROGRESS = "I"
    ON_HOLD = "O"
    DONE = "D"

class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    assignee = models.CharField(max_length=100)
    priority =  models.CharField(max_length=1, choices=Priority.choices, default=Priority.MEDIUM)
    time_unit = models.CharField(max_length=1, choices=TimeUnit.choices, default=TimeUnit.HOUR)
    estimate_time_to_complete = models.FloatField(null=True)
    reported_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=TaskStatus.choices, default=TaskStatus.TODO)
    hold_on_reason = models.CharField(max_length=100, null=True)
    completed_time = models.DateTimeField(null=True)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="task",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
    
class Gender(models.TextChoices):
    MALE = "M"    
    FEMALE = "F"
    OTHERS = "O"

class UserDetails(models.Model):
    dob = models.DateTimeField(null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, null=True)
    age = models.IntegerField(null=True)
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="userDetails",
        null=True,
        blank=True
    )
    profile_image = models.ImageField(
        upload_to="profile_images/",
        null=True,
        blank=True
    )
