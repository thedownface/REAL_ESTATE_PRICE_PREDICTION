from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Item,Category,OrderItem,Order

class HomeView(ListView):
    model=Category
    template_name='core/home.html'

class ItemDetailView(DetailView):
    model=Item
    template_name="core/product.html"

@login_required
def add_to_cart(request,slug):
    
    item=get_object_or_404( Item,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=100
            order_item.save()
            messages.info(request,'This Item quantity was updated')
        else:
            
            order.items.add(order_item)
            messages.info(request,'This Item was Succesfully added to your cart')
            return redirect("core:product",slug=slug)
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,'This Item was Succesfully added to your cart')
        return redirect("core:product",slug=slug)
    return redirect("core:product",slug=slug)
@login_required   
def remove_from_cart(request,slug):
    item=get_object_or_404( Item,slug=slug)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
                )[0]
            
            order.items.remove(order_item)
            messages.info(request,'This Item was Succesfully Removed from your cart')
        else:
            messages.info(request,'This Item was not in your cart')
            return redirect("core:product",slug=slug)
        

    else:
        messages.info(request,'You do not have an active order')
        return redirect("core:product",slug=slug)
    return redirect("core:product",slug=slug)


def joinus(request):
    return render(request,"core/joinus.html")

def logout_view(request):
    logout(request)
    return redirect('core:home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'core/login.html')