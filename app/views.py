from email import message
import random
from django import forms, views
from django.conf.urls.static import static
from django.contrib.auth import models,authenticate,get_user_model,login
from django.shortcuts import render, redirect
from django.views import View
from .models import Product,Customer,Cart,OrderPlaced,Profile
from .forms import CustomerRegistrationForm, LoginForm, ProfileViewForm
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import os
from twilio.rest import Client

User = get_user_model()

def sendotp(mobile,otp):
    #print(mobile)
    account_sid = 'AC981fc689582dba02533ecf781f25680b'
    auth_token = '8cf9746f52929a3d7f49d5a2aeeb1f54'
    client = Client(account_sid, auth_token)
    message = client.messages \
                .create(
                     body="Your otp is "+otp+" thank you",
                     from_='+18596462807',
                     to='+91'+mobile,
                 )

    print("haha",message.sid,message.body)



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
        item_in_cart= False
        if request.user.is_authenticated:
            item_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product,'item_in_cart':item_in_cart})

def show_square(request):
    return render(request,'app/square-payment2.html')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')
@login_required
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

@method_decorator(login_required, name="dispatch")
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
            city = form.cleaned_data['city']
            pincode = form.cleaned_data['pincode']
            state = form.cleaned_data['state']
            reg = Customer(user=usr,name=name,locality=locality,city=city,
            pincode=pincode,state=state)
            reg.save()
            messages.success(request,'Congratulations !! Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})
@login_required
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



def otp(request):
    mobile = request.session['mobile']
    username = request.session['username']
    password = request.session['password']
    context = {'mobile':mobile}
    #user = request.user
    #
    # print(user)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        #print(profile.otp," this",profile.user)
        

        if otp == profile.otp:
            messages.success(request, 'Congratulations!! otp validate Succesfully')
            print("successful")
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
                
        else:
            messages.error(request,"wrong otp")
            return render(request,'app/otp.html',context)
    return render(request,'app/otp.html',context)


@login_required
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

class LoginView(View):
    def get(self,request):
        form = LoginForm()
        return render(request,'app/login.html',{'form':form})

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username,"  ",password)
            user = authenticate(request,username=username,password=password)
            print(user)
            #print(request.user.is_authenticated())
            if user is not None:
                otp = str(random.randint(1000,9999))
                print(otp)
                profile = Profile.objects.get(user=user)
                profile.otp=otp
                profile.save()
                mobile = profile.mobile
                print(mobile)
                sendotp(mobile,otp)
                request.session['mobile'] = mobile
                request.session['username'] = username
                request.session['password'] = password
                return redirect('otp')
            
            else:
                print("not authenticated")
                messages.error(request,"username and password not valid ")
                return redirect('login')
           
        return render(request,'app/login.html',{'form':form})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            #print(mobile)
            user = User(name=name,email=email)
            user.set_password(password)
            user.save()
            # otp = str(random.randint(1000,9999))
            # print(otp)
            profile = Profile(user=user,mobile=mobile)
            profile.save()
            return redirect('login')
            
        return render(request, 'app/customerregistration.html', {'form':form})
