from django import forms
from .models import Patient, Prescription
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__' 
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        exclude = ["patient", "created_at"]
        widgets = {
            'exp_date': forms.DateInput(attrs={'type': 'date'}),
            'controlled': forms.CheckboxInput(),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']