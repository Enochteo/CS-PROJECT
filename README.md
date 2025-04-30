# CS-PHARMACY – Mini Virtual Hospital System

This Django-based pharmacy module is part of a virtual 
hospital system for educational purposes. It simulates 
basic healthcare functionalities such as managing 
prescriptions, checking controlled drugs, and validating 
insurance billing.

## ✅ Features

- Register new patients
- Add, edit, and delete prescriptions
- Check for controlled substances and suggest 
alternatives
- Validate prescription dosage and route
- Authenticate users (login/logout)
- Send email confirmations
- Display insurance-adjusted billing

## 📁 Project Structure

CS-PHARMACY/ ├── core/ # Main Django app │ ├── 
templates/ # HTML templates │ ├── models.py # Patient 
and Prescription models │ ├── views.py # View logic 
│ ├── forms.py # Django forms ├── 
pharmacy_project/ # Project settings and URLs ├── 
static/ # Static assets ├── manage.py ├── 
db.sqlite3 └── README.md
## 🧪 Run Locally

```bash
git clone https://github.com/Enochteo/CS-PROJECT.gitcd CS-PROJECT
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver




