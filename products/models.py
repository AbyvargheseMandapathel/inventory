

# from django.db import models

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     stock = models.PositiveIntegerField()


# # Create your models here.

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    product_name = models.CharField(max_length=255)
    description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/')
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    stock_level = models.IntegerField()
    reorder_point = models.IntegerField()
    supplier_name = models.CharField(max_length=255)
    supplier_email = models.EmailField()
    supplier_contact = models.CharField(max_length=15)
    order_date = models.DateField()
    quantity = models.IntegerField()
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.product_name


class StockTransaction(models.Model):
    STOCK_IN = 'in'
    STOCK_OUT = 'out'

    TRANSACTION_TYPE_CHOICES = [
        (STOCK_IN, 'Stock In'),
        (STOCK_OUT, 'Stock Out'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} - {self.quantity}"

