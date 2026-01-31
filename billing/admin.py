from django.contrib import admin
from .models import Product, Bill, BillItem


# ======================
# PRODUCT ADMIN
# ======================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)


# ======================
# BILL ITEM INLINE
# ======================
class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 0
    readonly_fields = ("product_name", "quantity", "price", "total")


# ======================
# BILL ADMIN
# ======================
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total_amount")
    list_filter = ("created_at",)
    inlines = [BillItemInline]
