from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product/', blank=True)

    def __str__(self):
        return self.name

class Bill(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total(self):
        # Explicitly aggregate from database to avoid stale instance data
        items = self.items.all()
        total = sum(item.total for item in items)
        self.total_amount = total
        self.save()

    def __str__(self):
        return f"Bill #{self.id}"

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate total before database write
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"
