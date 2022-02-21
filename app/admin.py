from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import  Customer, Product,Cart,OrderPlaced,Profile
# Register your models here.
User = get_user_model()

admin.site.register(User)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'pincode', 'state']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description',
    'brand', 'category', 'product_image']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'order_date', 'status']

@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['id','user','mobile','otp']