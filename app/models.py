from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATES_CHOICES = (
    ('Delhi','Delhi'),
    ('Bihar','Bihar'),
    ('Jharkhand','Jharkhand'),
    ('West Bengal','West Bengal'),
    ('Assam','Assam'),
    ('Chandigarh','Chandigarh')
)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    mobile_no = models.IntegerField()
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    state = models.CharField(choices=STATES_CHOICES, max_length=50)
    def __str__(self):
        return str(self.id)

CATEGORY_TYPE = (
    ('M','Mobile'),
    ('L','Laptop'),
    ('UW','Upper Wear'),
    ('BW','Bottom Wear')
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_TYPE,max_length=2)
    product_image = models.ImageField(upload_to='productimg')
    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)
    
    @property
    def total_price(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICE,max_length=50,default='pending')

    def __str__(self):
        return str(self.id)
    
    @property
    def total_price(self):
        return self.quantity * self.product.discounted_price