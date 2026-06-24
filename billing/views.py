from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from datetime import datetime
from .models import Bill, BillItem

# ========== BILLING PAGE ==========
@require_http_methods(["GET"])
def billing_page(request):
    """Render the main billing page with all products"""
    from .models import Product  # Your product model
    
    products = Product.objects.all().order_by('name')
    context = {
        'products': products
    }
    return render(request, 'billing/billing_page.html', context)

# ========== SAVE BILL ==========
@require_http_methods(["POST"])
def save_bill(request):
    """Save a new bill with items"""
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        total = data.get('total', 0)

        if not items:
            return JsonResponse({
                'status': 'error',
                'message': 'No items in bill'
            })

        # Create bill record
        bill = Bill.objects.create(
            total_amount=total,
        )

        # Create bill items
        for item in items:
            BillItem.objects.create(
                bill=bill,
                product_name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
                total=item['price'] * item['quantity']
            )

        return JsonResponse({
            'status': 'success',
            'message': 'Bill saved successfully',
            'bill_id': bill.id
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

# ========== GET ALL BILLS ==========
@require_http_methods(["GET"])
def get_bills(request):
    """Get all bills for the reports page"""
    try:
        bills = Bill.objects.all().order_by('-created_at')

        bills_data = []
        for bill in bills:
            items = BillItem.objects.filter(bill=bill).values()
            bills_data.append({
                'id': bill.id,
                'date': bill.created_at.strftime('%d-%m-%Y'),
                'time': bill.created_at.strftime('%H:%M:%S'),
                'total_amount': bill.total_amount,
                'items': list(items)
            })

        return JsonResponse({
            'status': 'success',
            'bills': bills_data
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

# ========== DELETE BILL ==========
@require_http_methods(["DELETE"])
def delete_bill(request, bill_id):
    """Delete a specific bill and its items"""
    try:
        bill = Bill.objects.get(id=bill_id)
        
        # Delete associated items first (due to FK constraint)
        BillItem.objects.filter(bill=bill).delete()
        
        # Delete the bill
        bill.delete()

        return JsonResponse({
            'status': 'success',
            'message': 'Bill deleted successfully'
        })

    except Bill.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Bill not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

# ========== REPORTS PAGE ==========
@require_http_methods(["GET"])
def reports_page(request):
    """Render the reports page"""
    return render(request, 'sales_report/report.html')
