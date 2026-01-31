import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone
from billing.models import Bill, BillItem
from .models import SalesReport

@csrf_exempt
def save_bill(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            with transaction.atomic():
                # 1. Create the Bill
                bill = Bill.objects.create(total_amount=0)

                # 2. Create Bill Items
                for item in data.get("items", []):
                    BillItem.objects.create(
                        bill=bill,
                        product_name=item["name"], # This matches the JS 'name' key above
                        price=item["price"],
                        quantity=item["quantity"]
                    )


                # 3. Finalise Bill Total (runs the Bill's save logic)
                bill.calculate_total()

                # 4. Update the Daily Sales Report
                today = timezone.now().date()
                # Get or create the report object for today
                report, created = SalesReport.objects.get_or_create(date=today)
                # Recalculate and save the total
                report.update_daily_total()

            return JsonResponse({
                "status": "success",
                "bill_id": bill.id,
                "daily_total": float(report.daily_total)
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
