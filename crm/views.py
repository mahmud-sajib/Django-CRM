from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users, admin_only


from django.contrib import messages

from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
# Create your views here.

# Register View
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + username + '. Please login.')
            return redirect('login')

    context = {'form':form}
    return render(request, 'crm/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'crm/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


# Home Page (Admin only) View
@login_required(login_url="login")
@admin_only
def home(request):
    customers = Customer.objects.all()
    total_customers = customers.count() 
    
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()

    context = {
        'customers':customers, 
        'total_customers':total_customers, 
        'orders':orders, 
        'total_orders':total_orders,
        'delivered_orders':delivered_orders,
        'pending_orders':pending_orders 
    }
    
    return render(request, 'crm/dashboard.html', context)

# Individual Customer Page (Admin only) View
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    print(f"orders {orders}")
    orders_count = orders.count()


    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    print(f"ORDERS {orders}")

    context = {
        'customers':customers,
        'orders':orders, 
        'orders_count':orders_count, 
        'myFilter':myFilter
    }

    return render(request, 'crm/customer.html', context)

# Prodcut Listing Page (Admin only) View
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'crm/products.html', {'products':products})

# Order Create Page (Admin only) View
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = OrderForm()

    context = {
        'form':form
    }
    return render(request, 'crm/order-form.html', context)

# Order Update Page (Admin only) View
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
        form = OrderForm(request.POST or None, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = OrderForm(instance=order)
        context = {'form':form}
        return render(request, 'crm/order-form-update.html', context)

# Order Delete Page (Admin only) View
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order_item = Order.objects.get(id=pk)
    order_item.delete()
    return redirect('home')

# Customer Dashboard (Customer only) Page View
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()
    
    context = {
        'orders':orders, 
        'total_orders':total_orders,
        'delivered_orders':delivered_orders,
        'pending_orders':pending_orders
    }
    
    return render(request, 'crm/user.html', context)

# Customer Profile (Customer only) Page View
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST or None, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('user-page')

    context = {'form':form}
    return render(request, 'crm/account_settings.html', context)