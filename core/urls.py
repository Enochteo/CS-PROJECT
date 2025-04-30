# core/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.new_patient, name='register_patient'),
    path('search/', views.search_patient, name='search_patient'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:patient_id>/add-prescription/', views.add_prescription, name='add_prescription'),

    # Auth views
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('prescription/<int:pk>/edit/', views.edit_prescription, name='edit_prescription'),
    path('prescription/<int:pk>/delete/', views.delete_prescription, name='delete_prescription'),
    path('prescription/<int:pk>/edit/', views.edit_prescription, name='edit_prescription'),
    path('prescription/<int:pk>/delete/', views.delete_prescription, name='delete_prescription'),
    path('pharmacy-location/', views.show_nearest_pharmacy, name='pharmacy_location'),

]
