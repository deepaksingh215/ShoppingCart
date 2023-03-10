from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustmerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ProductView(View):
    def get(self, request): 
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', 
            {'topwears': topwears,
            'mobiles': mobiles, 'laptops': laptops, 'totalitem': totalitem})


class ProductDetailView(View): 
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter( Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'app/productdetail.html', 
            {
                'product': product, 
                'item_already_in_cart': item_already_in_cart, 
                'totalitem': totalitem
            }
        )

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    
    Cart(user=user, product=product).save()
    return redirect ('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
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
                {'carts': cart, 'total_amount': total_amount, 'amount': amount, 'totalitem': totalitem})

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


# @login_required
# def buy_now(request):
    
#     return render(request, 'app/buynow.html')

@login_required
def orders(request):
    totalitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html' ,{'order_placed':op, 'totalitem':totalitem} )  



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

@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
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
    {'add': add, 'cart_items': cart_items, 'total_amount': total_amount, 'totalitem': totalitem})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    # customer = Customer.objects.get(id=custid)
    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        messages.error(request, 'Error: Select an address to deliver your orders' )
        return redirect('checkout')
    
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, 
        product=c.product, quantity=c.quantity).save()
        c.delete()
    messages.success(request, 'Order placed successfully')
    return redirect('orders')

@method_decorator(login_required, name='dispatch')
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

@login_required
def address(request):
    totalitem  = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add,'active': 'btn-primary', 'totalitem':totalitem})