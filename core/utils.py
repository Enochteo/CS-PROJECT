import csv
import json

CONTROLLED_DRUGS_LIST = [
    "amphetamines", "fentanyl", "morphine", "oxycodone", "hydrocodone", "adderall"
]

SUBSTITUTES = {
    "fentanyl": "acetaminophen",
    "morphine": "ibuprofen",
    "oxycodone": "naproxen",
    "hydrocodone": "tramadol",
    "adderall": "atomoxetine"
}

DRUG_PRICES = {
    "acetaminophen": 10.00,
    "ibuprofen": 12.00,
    "naproxen": 14.50,
    "tramadol": 9.00,
    "atomoxetine": 11.75
}

def is_controlled_substance(drug_name):
    return drug_name.lower() in CONTROLLED_DRUGS_LIST

def substitute_drug(drug_name):
    return SUBSTITUTES.get(drug_name.lower(), drug_name)

def get_price(drug_name):
    return DRUG_PRICES.get(drug_name.lower(), 0.0)

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

            row['price'] = get_price(row['substituted'])
            updated.append(row)
    return updated
