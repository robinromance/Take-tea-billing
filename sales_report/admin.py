from django.contrib import admin
from .models import SalesReport

@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    # Only use fields that exist in your new model
    list_display = ('date', 'daily_total') 
