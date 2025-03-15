from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, F
from shop.models import Product


# Create your models here.
class CartPro(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.name

    def subtotal(self):
        return self.product.price * self.quantity

    def get_total_price(self):
        total = 0
        total = total + (Sum(F('product.price') * F('quantity')))
        return total


class Order_detail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_items = models.IntegerField()
    street_address = models.TextField()
    city = models.TextField()
    province = models.TextField()
    country = models.TextField()
    postal_code = models.TextField()
    phone_number = models.BigIntegerField()
    order_id = models.CharField(max_length=30)
    payment_status = models.CharField(max_length=30,default="pending")
    delivery_status = models.CharField(max_length=30,default="pending")
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

class Payment(models.Model):
    name = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    order_id = models.CharField(max_length=30)
    razorpay_payment_id = models.CharField(max_length=30,blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.order_id