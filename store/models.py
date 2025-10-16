from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # ✅ Add this
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)      # ✅ Timestamp for updates

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # ✅ Yoco token
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"
