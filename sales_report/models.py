from django.db import models
from django.db.models import Sum

class SalesReport(models.Model):
    # This stores the specific day for the report
    date = models.DateField(unique=True)
    # The total sum of all bills for this day
    daily_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def update_daily_total(self):
        """
        Calculates the sum of all Bills created on this date.
        """
        from billing.models import Bill
        # Sum total_amount from all Bills where created_at date matches this report's date
        daily_sum = Bill.objects.filter(created_at__date=self.date).aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        self.daily_total = daily_sum
        self.save()

    def __str__(self):
        return f"Sales Report - {self.date}"

