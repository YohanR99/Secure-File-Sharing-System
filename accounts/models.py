from django.db import models
from django.contrib.auth.models import User

# Department choices
DEPARTMENTS = [
    ('IT', 'IT'),
    ('HR', 'HR'),
    ('Finance', 'Finance'),
    ('Admin', 'Admin'),
]

# Role choices
ROLES = [
    ('Manager', 'Manager'),
    ('Staff', 'Staff'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} Profile"
        
        
# ✅ Department model for user grouping
class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name