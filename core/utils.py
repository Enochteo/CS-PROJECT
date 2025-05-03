import csv
import json
import os
from django.conf import settings
from django.core.mail import send_mail


"""CONTROLLED_DRUGS_LIST = [
    "amphetamines", "fentanyl", "morphine", "oxycodone", "hydrocodone", "adderall"
]

SUBSTITUTES = {
    "fentanyl": "acetaminophen",
    "morphine": "ibuprofen",
    "oxycodone": "naproxen",
    "hydrocodone": "tramadol",
    "adderall": "atomoxetine"
}"""

DRUG_PRICES = {
    "acetaminophen": 10.00,
    "ibuprofen": 12.00,
    "naproxen": 14.50,
    "tramadol": 9.00,
    "atomoxetine": 11.75,
    "Paracetamol": 5.00,
    "Ibuprofen": 8.00,
    "Amoxicillin": 12.00,
    "Atropine": 15.50,
    "Generic Eye Drops": 6.75,
    "Anti-Anxiety Med": 10.00,
    "Default": 9.99 
}

def load_controlled_substances():
    path = os.path.join(settings.BASE_DIR, 'core', 'controlled_substances.json')
    with open(path, 'r') as f:
        return json.load(f)

def load_substitution_data():
    path = os.path.join(settings.BASE_DIR, 'data', 'drug_substitutions.json')
    with open(path, 'r') as file:
        return json.load(file)

def is_controlled_substance(drug_name):
    data = load_substitution_data()
    return any(d['original'].lower() == drug_name.lower() for d in data)

def substitute_drug(drug_name):
    data = load_substitution_data()
    for d in data:
        if d['original'].lower() == drug_name.lower():
            return d['substitute']
    return drug_name

def calculate_price(drug_name):
    return DRUG_PRICES.get(drug_name, DRUG_PRICES['Default'])

def pharmacy_lookup(zip_code):
    # Mock function – replace with actual API in production
    return f"Closest pharmacy for ZIP {zip_code}: CVS near Main St."

def process_prescription_csv(file_path):
    updated = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            drug = row['medication']
            if is_controlled_substance(drug):
                row['substituted'] = substitute_drug(drug)
            else:
                row['substituted'] = drug

            if not row.get('dosage'):
                row['error'] = "Missing dosage"

            row['price'] = calculate_price(row['substituted'])
            updated.append(row)
    return updated

def send_prescription_email(patient_email, patient_name, prescription):
    subject = f"Your Prescription from CS-Pharmacy"
    message = f"""
Hello {patient_name},

Your prescription for {prescription.medication_name} has been prepared.

Details:
- Dosage: {prescription.dosage}
- Directions: {prescription.directions}
- Price: ${prescription.price}

Please contact us if you have questions.

Best regards,  
CS-Pharmacy Team
"""
    send_mail(subject, message, None, [patient_email])
