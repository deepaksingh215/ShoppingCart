from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustmerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy


# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self, request): 
        topwears = Product.objects.filter(category='TW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request, 'app/home.html', 
            {'topwears': topwears,
            'mobiles': mobiles, 'laptops': laptops})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View): 
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product': product})


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    
    Cart(user=user, product=product).save()
    return redirect ('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discount_price)
                amount = amount + temp_amount
                total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', 
                {'carts': cart, 'total_amount': total_amount, 'amount': amount})

        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount = amount + temp_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount = amount + temp_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount = amount + temp_amount

        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)





def buy_now(request):
 return render(request, 'app/buynow.html')

def orders(request):
 return render(request, 'app/orders.html')

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'apple' or data == 'oneplus' or data == 'vivo' or data == 'realme' or  data == 'moto':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discount_price__lte=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discount_price__gte=10000)

    return render(request, 'app/mobile.html' , {'mobiles': mobiles})

def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discount_price__lte=50000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discount_price__gte=50000)

    return render(request, 'app/laptops.html' , {'laptops': laptops})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Registration Successful')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]    

    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount
        total_amount = amount + shipping_amount

    return render(request, 'app/checkout.html', 
    {'add': add, 'cart_items': cart_items, 'total_amount': total_amount})


class ProfileView(View):
    def get(self, request):
        form = CustmerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    
    def post(self, request):
        form = CustmerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data.get('name')
            locality = form.cleaned_data.get('locality')
            city = form.cleaned_data.get('city')
            zipcode = form.cleaned_data.get('zipcode') 
            state = form.cleaned_data.get('state')
            
            res = Customer(user=usr, name=name, locality=locality, city=city, zipcode=zipcode, state=state)
            res.save()
            messages.success(request, 'Congrutulations, you have successfully updated your profile')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add,'active': 'btn-primary'})