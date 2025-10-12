from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=100, blank=True, null=True, help_text="User's region for popularity tracking")
    
    def __str__(self):
        return f"{self.user.username} - {self.region or 'No region'}"

# Create your models here.
