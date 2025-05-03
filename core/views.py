from django.shortcuts import render, redirect
from .forms import PatientForm, PrescriptionForm
from .models import Patient, Prescription
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from .utils import is_controlled_substance, substitute_drug, calculate_price, pharmacy_lookup, send_prescription_email
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.http import HttpResponseForbidden
from .models import Prescription
from django.contrib import messages

# Create your views here.
@login_required
def home(request):
    return render(request, "core/home.html")

@login_required
def new_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_patient')  
    else:
        form = PatientForm()

    return render(request, 'core/new_patient.html', {'form': form})

@login_required
def search_patient(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Patient.objects.filter(name__icontains=query)

    return render(request, 'core/search_patient.html', {'results': results})

@login_required
def patient_detail(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    prescriptions = Prescription.objects.filter(patient=patient)
    return render(request, 'core/patient_detail.html', {
        'patient': patient,
        'prescriptions': prescriptions})

@login_required
def add_prescription(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient

            med_name = prescription.medication_name

            # Substitute if it's controlled
            if is_controlled_substance(med_name):
                substituted = substitute_drug(med_name)
                prescription.medication_name = substitute_drug(med_name)
                messages.warning(request, f"'{med_name}' is a controlled substance. It was substituted with '{substituted}'.")
            # Set the price
            prescription.price = calculate_price(prescription.medication_name)

            prescription.save()
            return redirect('patient_detail', patient_id=patient.id)
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        form = PrescriptionForm()

    return render(request, 'core/add_prescription.html', {'form': form, 'patient': patient})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def edit_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=prescription.patient.id)
    else:
        form = PrescriptionForm(instance=prescription)

    return render(request, 'core/edit_prescription.html', {
        'form': form,
        'prescription': prescription,
        'patient': prescription.patient
    })

@login_required
def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    patient_id = prescription.patient.id
    prescription.delete()
    return redirect('patient_detail', patient_id=patient_id)

@login_required
def show_nearest_pharmacy(request):
    zip_code = request.GET.get('zip')
    location = pharmacy_lookup(zip_code)
    return render(request, 'core/pharmacy_location.html', {'location': location})

@login_required
def send_to_pharmacy(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    prescription.sent_to_pharmacy = True
    prescription.verified_by_pharmacy = False  # Simulate initial pending state
    prescription.verified_at = None
    prescription.save()
    return redirect('patient_detail', patient_id=prescription.patient.id)

@login_required
def verify_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if not prescription.sent_to_pharmacy:
        return HttpResponseForbidden("Cannot verify a prescription that hasn't been sent.")
    prescription.verified_by_pharmacy = True
    prescription.save()
    patient = prescription.patient
    if patient.email:
        send_prescription_email(patient.email, patient.name, prescription)    
    messages.success(request, f"Prescription for '{prescription.medication_name}' has been verified and prescription has been sent to the Patient.")
    return redirect('patient_detail', patient_id=prescription.patient.id)

def mark_as_sent(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    prescription.sent_to_pharmacy = True
    prescription.save()
    messages.info(request, f"Prescription for '{prescription.medication_name}' has been sent to the pharmacy.")
    return redirect('patient_detail', patient_id=prescription.patient.id)
@login_required
def pharmacy_dashboard(request):
    prescriptions = Prescription.objects.filter(sent_to_pharmacy=True)
    return render(request, 'core/pharmacy_dashboard.html', {
        'prescriptions': prescriptions
    })

class CustomLoginView(LoginView):
    template_name = 'core/login.html'

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            # Session expires at browser close
            self.request.session.set_expiry(0)
        else:
            # Default expiry (e.g. 2 weeks)
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)
    
