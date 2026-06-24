# ========== urls.py ==========
"""
Add these URLs to your Django app's urls.py
"""

from django.urls import path
from . import views

urlpatterns = [
    # Billing page
    path('', views.billing_page, name='billing'),
    
    # API endpoints
    path('save-bill/', views.save_bill, name='save_bill'),
    path('get-bills/', views.get_bills, name='get_bills'),
    path('delete-bill/<int:bill_id>/', views.delete_bill, name='delete_bill'),
    
    # Reports page
    path('reports/', views.reports_page, name='reports'),
]

