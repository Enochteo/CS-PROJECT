# Register your models here.
from django.contrib import admin
from .models import Patient, Pharmacy, Prescription, Allergy, ReportedInfo

admin.site.register(Patient)
admin.site.register(Pharmacy)
admin.site.register(Prescription)
admin.site.register(Allergy)
admin.site.register(ReportedInfo)
