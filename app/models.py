from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser
from django.conf import settings



class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):
        
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, password, **other_fields)




    def create_user(self, email, name, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    # Summary tab
    
    
    # account_name is not changeable
    
    # account_name = models.ForeignKey('Account', blank=True, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(unique=True)
   

    name = models.CharField(max_length=150)  # Don't show this field.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # class Meta:
    #     verbose_name = ('user')
    #     verbose_name_plural = ('users')

    def __str__(self):
        return self.name





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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
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

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=12,unique=True,blank=False)
    otp = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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


