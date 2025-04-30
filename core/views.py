from django.shortcuts import render, redirect
from .forms import PatientForm, PrescriptionForm
from .models import Patient, Prescription
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from .utils import is_controlled_substance, substitute_drug, get_price, pharmacy_lookup

# Create your views here.

def home(request):
    return render(request, "core/home.html")

def new_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_patient')  # You can change this later
    else:
        form = PatientForm()

    return render(request, 'core/new_patient.html', {'form': form})

def search_patient(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Patient.objects.filter(name__icontains=query)

    return render(request, 'core/search_patient.html', {'results': results})

def patient_detail(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    prescriptions = Prescription.objects.filter(patient=patient)
    return render(request, 'core/patient_detail.html', {
        'patient': patient,
        'prescriptions': prescriptions})

def add_prescription(request, patient_id):
    from django.http import HttpResponse
    patient = Patient.objects.get(id=patient_id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient
            prescription.save()
            print("Redirecting to patient detail for ID:", patient.id)
            return redirect('patient_detail', patient_id=patient.id)
        else:
            print("Form is invalid")
            print(form.errors)
    else:    
        form = PrescriptionForm()
    if is_controlled_substance(form.cleaned_data['medication_name']):
        form.instance.medication_name = substitute_drug(form.cleaned_data['medication_name'])
    form.instance.price = get_price(form.instance.medication_name)

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


def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    patient_id = prescription.patient.id
    prescription.delete()
    return redirect('patient_detail', patient_id=patient_id)

def show_nearest_pharmacy(request):
    zip_code = request.GET.get('zip')
    location = pharmacy_lookup(zip_code)
    return render(request, 'core/pharmacy_location.html', {'location': location})
