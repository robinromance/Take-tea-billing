import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Product, Bill, BillItem
from sales_report.models import SalesReport
from django.views.decorators.csrf import csrf_exempt


def billing_page(request):
    products = Product.objects.all()
    return render(request, "billing/billing_page.html", {"products": products})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_bill(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)

        items = data.get("items", [])
        total = data.get("total", 0)

        print("ITEMS:", items)
        print("TOTAL:", total)

        return JsonResponse({
            "status": "success"
        })

    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

