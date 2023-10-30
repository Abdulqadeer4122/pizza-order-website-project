from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import login, authenticate, logout
# Create your views here.

def home(request):
    pizzas = Pizza.objects.all()
    return render(request, 'home.html', {'pizzas': pizzas})


def add_cart(request, pizza_id):
    user = request.user
    pizza_obj = Pizza.objects.get(uid=pizza_id)
    cart,_ = Cart.objects.get_or_create(user=user,is_paid=False)
    cart_item=CartItems(cart_user=cart, piza=pizza_obj)
    cart_item.save()
    return redirect('/')
@login_required
def cart(request):
    cart_list=Cart.objects.get(is_paid=False,user=request.user)

    return render(request, 'cart_list.html',
                  {"cart_list": cart_list})

def remove_cart_item(request, cart_item_uid):
    CartItems.objects.get(uid=cart_item_uid).delete()
    return redirect('/cart/')

def order(request):
    orders=Cart.objects.filter(is_paid=True, user=request.user)
    return render(request, 'order.html', {'orders':orders})

def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('passwrd')
            user = User.objects.filter(username=username)
            if not user.exists():
                messages.error(request, 'User not found')
                return redirect('/login/')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            messages.error(request, 'your password is wrong')
            return redirect('/login/')
        except Exception as e:
            messages.error(request, 'Something went wrong')
            return redirect('/login/')
    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('passwrd')
        username=request.POST.get('username')
        user=User.objects.filter(email=email)
        if user.exists():
            messages.error(request,'Email already exist')
            return redirect('/register/')
        user = User.objects.create(email=email,username=username)
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created')
        return redirect('/login/')
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect('/')
