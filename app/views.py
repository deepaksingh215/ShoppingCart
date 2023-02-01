from django.shortcuts import render
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustmerProfileForm
from django.contrib import messages

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
 return render(request, 'app/addtocart.html')

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
 return render(request, 'app/checkout.html')


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