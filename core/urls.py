# core/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    # Patient-related views
    path('register/', views.new_patient, name='register_patient'),
    path('search/', views.search_patient, name='search_patient'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:patient_id>/add-prescription/', views.add_prescription, name='add_prescription'),

    # Prescription editing and sending
    path('prescription/<int:pk>/edit/', views.edit_prescription, name='edit_prescription'),
    path('prescription/<int:pk>/delete/', views.delete_prescription, name='delete_prescription'),
    path('prescription/<int:pk>/send/', views.send_to_pharmacy, name='send_to_pharmacy'),
    path('prescription/<int:pk>/send/', views.send_to_pharmacy, name='send_to_pharmacy'),
    path('prescription/<int:pk>/verify/', views.verify_prescription, name='verify_prescription'),
    path('prescription/<int:pk>/send/', views.mark_as_sent, name='mark_as_sent'),

    # Optional: nearest pharmacy
    path('pharmacy-location/', views.show_nearest_pharmacy, name='pharmacy_location'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register-user/', views.register_user, name='register_user'),

    path('pharmacy-dashboard/', views.pharmacy_dashboard, name='pharmacy_dashboard'),

]
