from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    contact = models.CharField(max_length=50)
    address = models.TextField()
    insurance = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.date_of_birth})"

class Pharmacy(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Prescription(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Verified', 'Verified'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    condition = models.CharField(max_length=100, null=True, blank=True)
    pharmacy = models.CharField(max_length=100)
    medication_name = models.CharField(max_length=100)
    refill = models.PositiveIntegerField(null=True, blank=True)
    dosage = models.CharField(max_length=50)
    route = models.CharField(max_length=50)  # e.g., Oral, IV
    frequency = models.CharField(max_length=100)
    directions = models.TextField()
    dispense_unit = models.CharField(max_length=50)
    days_supply = models.IntegerField(null=True, blank=True)
    exp_date = models.DateField(null=True, blank=True)
    controlled = models.BooleanField(null=True, blank=True)
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.medication_name} for {self.patient.name}"

class Allergy(models.Model):
    SEVERITY_CHOICES = [
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    drug = models.CharField(max_length=100)
    reaction = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)

    def __str__(self):
        return f"{self.drug} - {self.severity}"

class ReportedInfo(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    info = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.patient.name} on {self.date_reported.strftime('%Y-%m-%d')}"
