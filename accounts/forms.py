from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Department, ROLES  # ✅ Import Department model
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department"
    )
    role = forms.ChoiceField(choices=ROLES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        department = self.cleaned_data['department']
        role = self.cleaned_data['role']
        
        # ✅ Ensure the profile is created correctly
        Profile.objects.create(
            user=user,
            department=department,  # Already a Department instance
            role=role
        )
        return user
