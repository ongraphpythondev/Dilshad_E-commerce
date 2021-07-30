from django import forms, views
from django.conf.urls.static import static
from django.contrib.auth import models
from django.shortcuts import render, redirect
from django.views import View
from .models import Product,Customer,Cart,OrderPlaced
from .forms import CustomerRegistrationForm, ProfileViewForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

class ProductView(View):
    def get(self,request):
        topwear = Product.objects.filter(category='UW')
        bottomwear = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html',{'topwear':topwear,'bottomwear':bottomwear,
        'mobiles':mobiles})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        return render(request, 'app/productdetail.html',{'product':product})
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')
def showcart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user ]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+= tempamount

        return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':amount+shipping,'amount':amount})


def PlusCart(request):
    if request.method == "GET":
        prod_id = request.GET['proud_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user ]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+= tempamount

            data = {
                'amount':amount,
                'totalamount':amount + shipping,
                'quantity' : c.quantity
            }
        return JsonResponse(data)
def MinusCart(request):
    if request.method == "GET":
        prod_id = request.GET['proud_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user ]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+= tempamount

            data = {
                'amount':amount,
                'totalamount':amount + shipping,
                'quantity' : c.quantity
            }
        return JsonResponse(data)

def RemoveCart(request):
    if request.method == "GET":
        prod_id = request.GET['proud_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount

        data = {
            'amount':amount,
            'totalamount':amount + shipping
        }
        return JsonResponse(data)
            

def buy_now(request):
 return render(request, 'app/buynow.html')

class ProfleView(View):
    def get(self, request):
        form = ProfileViewForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self, request):
        usr = request.user
        form = ProfileViewForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            mobile_no = form.cleaned_data['mobile_no']
            city = form.cleaned_data['city']
            pincode = form.cleaned_data['pincode']
            state = form.cleaned_data['state']
            reg = Customer(user=usr,name=name,locality=locality,mobile_no=mobile_no,city=city,
            pincode=pincode,state=state)
            reg.save()
            messages.success(request,'Congratulations !! Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'realme' or data == 'POCO' or data == 'samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=15000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=15000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Succesfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount
        totalamount = amount+shipping
    return render(request, 'app/checkout.html',{'add':add, 'totalamount':totalamount,'cart_item':cart_items})
def Payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')
def CancelOrder(request):
    if request.method == 'GET':
        user = request.user
        op_id = request.GET['op_id']
        op = OrderPlaced.objects.get(id=op_id)
        op.delete()
        data={'deleted':'deleted'}
        return JsonResponse(data)