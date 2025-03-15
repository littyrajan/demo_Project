from django.contrib import admin

from cart.models import CartPro,Order_detail, Payment

# Register your models here.
admin.site.register(CartPro)
admin.site.register(Order_detail)
admin.site.register(Payment)