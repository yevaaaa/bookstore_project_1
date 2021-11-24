import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .utils import cookieCart, cartData, guestOrder
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Product
from .forms import CreateUserForm, ContactusForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# def registerPage(request):
#     if request.user.is_authenticated:
#         return redirect('store')
#     else:
#         form = CreateUserForm()
#
#         if request.method == 'POST':
#             form = CreateUserForm(request.POST)
#             if form.is_valid():
#                 user = form.cleaned_data.get('username')
#                 form.save()
#                 messages.success(request, 'Account was created for ' + user)
#
#                 return redirect('login')
#
#         context = {'form': form}
#         return render(request, 'bookstore/register.html', context)
#
#
# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect('store')
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 return redirect('store')
#             else:
#                 messages.info(request, 'Username or password is incorrect')
#
#         context = {}
#         return render(request, 'bookstore/login.html', context)

#
# def logoutUser(request):
#     logout(request)
#     return redirect('login')



def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    product_list = Product.objects.all().order_by('id')
    paginator = Paginator(product_list, 9)
    page_number = request.GET.get('page')
    paginator.get_page(page_number)
    page_obj = paginator.get_page(page_number)
    context = {'products': products, 'cartItems': cartItems, 'shipping': False, 'page_obj': page_obj}
    return render(request, 'bookstore/store.html', context)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'products'
    template_name = 'bookstore/product_detail.html'


# def productdetails(request,**kwargs):
#     data = cartData(request)
#     cartItems = data['cartItems']
#     order = data['order']
#     items = data['items']
#     products = Product.objects.all()
#     context = {'products':products, 'items': items, 'order': order, 'cartItems': cartItems,}
#     return render(request,'store/product_detail.html',context)
# @login_required(login_url='login')
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'bookstore/cart.html', context)


# @login_required(login_url='login')
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'bookstore/checkout.html', context)


# @login_required(login_url='login')
def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


# @csrf_exempt
# @login_required(login_url='login')
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAdress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            phone_number=data['shipping']['phone_number']
            # state=data['shipping']['state'],
            # zipcode=data['shipping']['zipcode']
        )

    return JsonResponse('Payment submitted..', safe=False)


# @login_required(login_url='login')
def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if request.method == 'POST':
        form = ContactusForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')

            subject = 'Someone contacted us'
            content = f"""
            {first_name} {last_name} is trying to contact u .
            Their email address is: {email}
            Message: {message}
            """

            send_mail(subject=subject, message=content,
                      from_email='shopforproject@gmail.com',
                      recipient_list=['shopforproject@gmail.com'])
            return redirect('thank_you')

    else:
        form = ContactusForm()
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'form': form}
    return render(request, 'bookstore/contact_us.html', context)


def thank_you(request):
    return render(request, 'bookstore/thank_you.html')
#
# @login_required(login_url='login')
def search_products(request):
    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(name__contains=searched)

        return render(request,
                      'bookstore/search_products.html',
                      {'searched': searched,
                       'products': products,
                       'cartItems': cartItems}
                      )
    else:
        return render(request,
                      'bookstore/search_products.html',
                      {})


def search(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'bookstore/search.html', context)
