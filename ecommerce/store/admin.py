from django.contrib import admin
from .models import Order, OrderItem, Product, ShippingAddress, ImageProduct
# Register your models here.


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(ImageProduct)