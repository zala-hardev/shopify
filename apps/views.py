import email
from math import prod
from turtle import color
from unicodedata import category
from urllib import request
from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Customer,Colors,WishList,Cart,OrderPlaced
import random
# pagination
from django.core.paginator import Paginator
# import json
from django.http import JsonResponse,HttpResponse
# class based function
from django.views import View
# django's form 
from .forms import CustomerRegistrationForm,CustomerProfileForm,ChangePasswordForm,CustomPasswordResetForm,ProductForm
# CustomerLoginForm
# django's message
from django.contrib import messages
# importing django's built-in User
from django.contrib.auth.models import User
# importing logout
from django.contrib.auth import logout,authenticate,login
# import login_required
from django.contrib.auth.decorators import login_required
# importing Q for complex querires
from django.db.models import Q
# importing heap for index page
import heapq
# importing razorpay for payment intergration
import razorpay
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# for invoice pdf genertor
from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.lib import colors
from django.templatetags.static import static
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password

# forgot password
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView,PasswordResetCompleteView,PasswordResetDoneView,PasswordResetConfirmView
from django.urls import reverse_lazy

# Home Page
# @login_required(login_url='login')
def home_Page(request):
  
  products = Product.objects.all()
  # sorting products according to it's price
  sorted_products = sorted(products,key=lambda x: x.total_discount,reverse=True)[:4]
  # wishlist = WishList.objects.all().select_related('product')

  return render(request,'index.html',{'items':sorted_products})

# WishList Items adding
@login_required(login_url='login')
def add_wishlist_items(request):
    product_id = request.GET.get('product_id')
    print(product_id)
    product = get_object_or_404(Product,id=product_id)
    # product = Product.objects.get(id=product_id)
    wishlist,created = WishList.objects.get_or_create(user=request.user,product=product)
    print(created)
    
    if not created:
      wishlist.delete()
      added = False
    
    else:
      added = True

    return JsonResponse({'added':added})


# info of each product
def product_details(request,pk):
  product_info = Product.objects.get(id=pk)
  reviews = random.randint(100,1000)
  # print(product_info)
  product_colors = product_info.colors.all()
  # colors_available = {color for color in product_colors}
  print(product_colors)

  # user's last visited page using middleware and session
  last_page = request.session.get('last_page', None)
  print(last_page)

  return render(request,'productDetails.html',{'item':product_info,'last_page':last_page,'reviews':reviews,'colors_varients':product_colors})

# Create your views here.
@login_required(login_url='login')
def contact(request):

  msg = ""

  if request.method == 'POST':

    form = CustomerProfileForm(request.POST)

    if form.is_valid():

      full_name = form.cleaned_data['customer_name']
      city = form.cleaned_data['customer_city']
      state = form.cleaned_data['customer_state']
      address = form.cleaned_data['customer_address']
      phone = form.cleaned_data['customer_phone']
      country = form.cleaned_data['customer_country']

      reg = Customer(user=request.user,customer_name=full_name,customer_phone=phone,customer_address=address,customer_city=city,customer_state=state,customer_country=country)      
      reg.save()

      msg = 'success'

    else:
      
      msg = 'error'

  else:

    form = CustomerProfileForm()

  return render(request,'contact.html',{'form':form,'msg':msg})

@login_required(login_url='login')
def add_cart_page(request):

  if request.method == 'POST':
    product_id = request.POST.get('product_id')
    product_color = request.POST.get('color_choice')
    cart_product = Cart(user=request.user,product=Product.objects.get(id=product_id),color=Colors.objects.get(color_name=product_color)) 
    cart_product.save()

  return redirect('/show-cart')

def show_cart_page(request):

  get_cart_products = Cart.objects.filter(user=request.user)
  amount = 0.0
  shipping = 2
  last_amount = 0.0

  if get_cart_products:
    for i in get_cart_products:
      amount += i.total_amount
    last_amount = shipping + amount 

  return render(request,'cart.html',{'cart_products':get_cart_products,'last_amount':last_amount,'is_cartExist':get_cart_products.exists()})

def plus_cart(request):

  if request.method == 'GET':

    id = request.GET.get('product_id')
    color = request.GET.get('product_color')
    product_color = Colors.objects.get(color_name=color)
    cart_product = Cart.objects.get(Q(user=request.user) & Q(product=Product.objects.get(id=id)) & Q(color=product_color))
    cart_product.quantity += 1
    cart_product.save()
    each_product_amount = cart_product.total_amount
    amount = 0.00
    shipping = 2.00
    last_amount = 0.00
    user_carted_products = [i for i in Cart.objects.all() if i.user == request.user]

    if user_carted_products:
      for i in user_carted_products:
        amount += i.total_amount
      
      last_amount = shipping + amount

    return JsonResponse({'quantity':cart_product.quantity,'last_amount':last_amount,'each_product_amount':each_product_amount})
  
def minus_cart(request):

  if request.method == 'GET':

    id = request.GET.get('product_id')
    color = request.GET.get('product_color')
    product_color = Colors.objects.get(color_name=color)

    cart_product = Cart.objects.get(Q(user=request.user) & Q(product=Product.objects.get(id=id)) & Q(color=product_color))
    if cart_product.quantity > 1:
      cart_product.quantity -= 1
    cart_product.save()
    each_product_amount = cart_product.total_amount
    amount = 0.00
    shipping = 2.00
    last_amount = 0.00
    user_carted_products = [i for i in Cart.objects.all() if i.user == request.user]

    if user_carted_products:
      for i in user_carted_products:
        amount += i.total_amount
      
      last_amount = shipping + amount

    return JsonResponse({'quantity':cart_product.quantity,'last_amount':last_amount,'each_product_amount':each_product_amount})

def remove_cart(request):

  if request.method == 'GET':

    id = request.GET.get('product_id')
    color = request.GET.get('product_color')
    cart_product = Cart.objects.get(Q(user=request.user) & Q(product=id) & Q(color=Colors.objects.get(color_name=color)))
    cart_product.delete()

    amount = 0.00
    shipping = 2.00
    last_amount = 0.00
    user_carted_products = [i for i in Cart.objects.all() if i.user == request.user]

    if user_carted_products:
      for i in user_carted_products:
        amount += i.total_amount
      last_amount = shipping + amount

    return JsonResponse({'last_amount':last_amount})


@login_required(login_url='login')
def profile_page(request):
  is_profile = Customer.objects.filter(user=request.user).exists()
  # print(is_profile)
  if is_profile:
    profile = Customer.objects.filter(user=request.user)
    paginator = Paginator(profile,1)
    pages = request.GET.get('pageOfprofile')
    total_page = 0

    try:
      profile_details = paginator.get_page(pages)
      total_page = profile_details.paginator.num_pages

    except:
      profile_details = paginator.get_page(1)

    return render(request,'profile.html',{'profile':profile_details,'page':range(2,total_page),'last_page':total_page,})

  else:
    return render(request,'profile.html',{'not_exist':True})

def shop_all_page(request):

  all_prods = Product.objects.all()
  brands = {b.brand for b in all_prods}

  if request.method == 'POST':
    brand_filters = request.POST.getlist('brand')
    price_filters = request.POST.get('price')
    print(price_filters)

    if brand_filters != []:

      filtered_products = Product.objects.filter(brand__in=brand_filters)

      if price_filters == 'below':
        filtered_products = filtered_products.filter(discounted_price__lt=500)
      elif price_filters == 'above':
        filtered_products = filtered_products.filter(discounted_price__gte=500)
      else:
        pass
    
    elif brand_filters == [] and price_filters is None:
          
      paginator = Paginator(all_prods,3)
      page = request.GET.get('page')
      total_pages = 0

      brands = {b.brand for b in all_prods} #set comprehension
      # print(brands)
      try:
        obj = paginator.get_page(page)
        total_pages = obj.paginator.num_pages
      except:
        obj = paginator.page(1)

      return render(request,'shop_all.html',{'objects':obj,'brands':brands,'pages':range(2,total_pages),'last_page':total_pages,'isFiltered':False,'isProductExist':True})

    else:  
      if price_filters == 'below':
        filtered_products = Product.objects.filter(discounted_price__lt=500)
      elif price_filters == 'above':
        filtered_products = Product.objects.filter(discounted_price__gte=500)
      
    return render(request,'shop_all.html',{'objects':filtered_products,'brands':brands,'isFiltered':True,'isProductExist':filtered_products.exists()})
    
  else:

    paginator = Paginator(all_prods,3)
    page = request.GET.get('page')
    total_pages = 0

    brands = {b.brand for b in all_prods} #set comprehension
    # print(brands)
    try:
      obj = paginator.get_page(page)
      total_pages = obj.paginator.num_pages
    except:
      obj = paginator.page(1)

    return render(request,'shop_all.html',{'objects':obj,'brands':brands,'pages':range(2,total_pages),'last_page':total_pages,'isFiltered':False,'isProductExist':True})

def shop_mobile_page(request):

  all_prods = Product.objects.filter(category='Mobiles')
  brands = {b.brand for b in all_prods}

  if request.method == 'POST':
    brand_filters = request.POST.getlist('brand')
    price_filters = request.POST.get('price')
    print(price_filters)

    if brand_filters != []:

      filtered_products = Product.objects.filter(Q(category='Mobiles') & Q(brand__in=brand_filters))

      if price_filters == 'below':
        filtered_products = filtered_products.filter(Q(category='Mobiles') & Q(discounted_price__lt=500))
      elif price_filters == 'above':
        filtered_products = filtered_products.filter(Q(category='Mobiles') & Q(discounted_price__gte=500))
      else:
        pass
    
    elif brand_filters == [] and price_filters is None:
          
      paginator = Paginator(all_prods,3)
      page = request.GET.get('page')
      total_pages = 0

      brands = {b.brand for b in all_prods} #set comprehension
      # print(brands)
      try:
        obj = paginator.get_page(page)
        total_pages = obj.paginator.num_pages
      except:
        obj = paginator.page(1)

      return render(request,'shop_mobile.html',{'objects':obj,'brands':brands,'pages':range(2,total_pages),'last_page':total_pages,'isFiltered':False,'isProductExist':True})

    else:  
      if price_filters == 'below':
        filtered_products = Product.objects.filter(Q(category='Mobiles') & Q(discounted_price__lt=500))
      elif price_filters == 'above':
        filtered_products = Product.objects.filter(Q(category='Mobiles') & Q(discounted_price__gte=500))
      
    return render(request,'shop_mobile.html',{'objects':filtered_products,'brands':brands,'isFiltered':True,'isProductExist':filtered_products.exists()})
    
  else:

    paginator = Paginator(all_prods,3)
    page = request.GET.get('page')
    total_pages = 0

    brands = {b.brand for b in all_prods} #set comprehension
    # print(brands)
    try:
      obj = paginator.get_page(page)
      total_pages = obj.paginator.num_pages
    except:
      obj = paginator.page(1)

    return render(request,'shop_mobile.html',{'objects':obj,'brands':brands,'pages':range(2,total_pages),'last_page':total_pages,'isFiltered':False,'isProductExist':True})
  
def shop_laptop_page(request):

  all_prods = Product.objects.filter(category='Laptops')
  brands = {b.brand for b in all_prods}

  if request.method == 'POST':
    brand_filters = request.POST.getlist('brand')
    price_filters = request.POST.get('price')
    print(price_filters)

    if brand_filters != []:

      filtered_products = Product.objects.filter(Q(category='Laptops') & Q(brand__in=brand_filters))

      if price_filters == 'below':
        filtered_products = filtered_products.filter(Q(category='Laptops') & Q(discounted_price__lt=500))
      elif price_filters == 'above':
        filtered_products = filtered_products.filter(Q(category='Laptops') & Q(discounted_price__gte=500))
      else:
        pass
    
    elif brand_filters == [] and price_filters is None:
          
      paginator = Paginator(all_prods,3)
      page = request.GET.get('page')
      total_pages = 0

      brands = {b.brand for b in all_prods} #set comprehension
      # print(brands)
      try:
        obj = paginator.get_page(page)
        total_pages = obj.paginator.num_pages
      except:
        obj = paginator.page(1)

      return render(request,'shop_laptop.html',{'objects':obj,'brands':brands,'pages':range(2,total_pages),'last_page':total_pages,'isFiltered':False,'isProductExist':True})

    else:  
      if price_filters == 'below':
        filtered_products = Product.objects.filter(Q(category='Laptops') & Q(discounted_price__lt=500))
      elif price_filters == 'above':
        filtered_products = Product.objects.filter(Q(category='Laptops') & Q(discounted_price__gte=500))
      
    return render(request,'shop_laptop.html',{'objects':filtered_products,'brands':brands,'isFiltered':True,'isProductExist':filtered_products.exists()})
    
  else:

    paginator = Paginator(all_prods,3)
    page = request.GET.get('page')
    total_pages = 0

    brands = {b.brand for b in all_prods} #set comprehension
    # print(brands)
    try:
      obj = paginator.get_page(page)
      total_pages = obj.paginator.num_pages
    except:
      obj = paginator.page(1)

    return render(request,'shop_laptop.html',{'objects':obj,'brands':brands,'pages':range(2,total_pages),'last_page':total_pages,'isFiltered':False,'isProductExist':True})
  

def shop_smartwatch_page(request):

  all_prods = Product.objects.filter(category='Smartwatches')
  brands = {b.brand for b in all_prods}

  if request.method == 'POST':
    brand_filters = request.POST.getlist('brand')
    price_filters = request.POST.get('price')
    print(price_filters)

    if brand_filters != []:

      filtered_products = Product.objects.filter(Q(category='Smartwatches') & Q(brand__in=brand_filters))

      if price_filters == 'below':
        filtered_products = filtered_products.filter(Q(category='Smartwatches') & Q(discounted_price__lt=500))
      elif price_filters == 'above':
        filtered_products = filtered_products.filter(Q(category='Smartwatches') & Q(discounted_price__gte=500))
      else:
        pass
    
    elif brand_filters == [] and price_filters is None:
          
      paginator = Paginator(all_prods,3)
      page = request.GET.get('page')
      total_pages = 0

      brands = {b.brand for b in all_prods} #set comprehension
      # print(brands)
      try:
        obj = paginator.get_page(page)
        total_pages = obj.paginator.num_pages
      except:
        obj = paginator.page(1)

      return render(request,'shop_smartwatch.html',{'objects':obj,'brands':brands,'pages':range(2,total_pages),'last_page':total_pages,'isFiltered':False,'isProductExist':True})

    else:  
      if price_filters == 'below':
        filtered_products = Product.objects.filter(Q(category='Smartwatches') & Q(discounted_price__lt=500))
      elif price_filters == 'above':
        filtered_products = Product.objects.filter(Q(category='Smartwatches') & Q(discounted_price__gte=500))
      
    return render(request,'shop_smartwatch.html',{'objects':filtered_products,'brands':brands,'isFiltered':True,'isProductExist':filtered_products.exists()})
    
  else:

    paginator = Paginator(all_prods,3)
    page = request.GET.get('page')
    total_pages = 0

    brands = {b.brand for b in all_prods} #set comprehension
    # print(brands)
    try:
      obj = paginator.get_page(page)
      total_pages = obj.paginator.num_pages
    except:
      obj = paginator.page(1)

    return render(request,'shop_smartwatch.html',{'objects':obj,'brands':brands,'pages':range(2,total_pages),'last_page':total_pages,'isFiltered':False,'isProductExist':True})


def shop_headphones_page(request):

  all_prods = Product.objects.filter(category='Headphones')
  brands = {b.brand for b in all_prods}

  if request.method == 'POST':
    brand_filters = request.POST.getlist('brand')
    price_filters = request.POST.get('price')
    print(price_filters)

    if brand_filters != []:

      filtered_products = Product.objects.filter(Q(category='Headphones') & Q(brand__in=brand_filters))

      if price_filters == 'below':
        filtered_products = filtered_products.filter(Q(category='Headphones') & Q(discounted_price__lt=300))
      elif price_filters == 'above':
        filtered_products = filtered_products.filter(Q(category='Headphones') & Q(discounted_price__gte=300))
      else:
        pass
    
    elif brand_filters == [] and price_filters is None:
          
      paginator = Paginator(all_prods,3)
      page = request.GET.get('page')
      total_pages = 0

      brands = {b.brand for b in all_prods} #set comprehension
      # print(brands)
      try:
        obj = paginator.get_page(page)
        total_pages = obj.paginator.num_pages
      except:
        obj = paginator.page(1)

      return render(request,'shop_headphones.html',{'objects':obj,'brands':brands,'pages':range(2,total_pages),'last_page':total_pages,'isFiltered':False,'isProductExist':True})

    else:  
      if price_filters == 'below':
        filtered_products = Product.objects.filter(Q(category='Headphones') & Q(discounted_price__lt=300))
      elif price_filters == 'above':
        filtered_products = Product.objects.filter(Q(category='Headphones') & Q(discounted_price__gte=300))
      
    return render(request,'shop_headphones.html',{'objects':filtered_products,'brands':brands,'isFiltered':True,'isProductExist':filtered_products.exists()})
    
  else:

    paginator = Paginator(all_prods,3)
    page = request.GET.get('page')
    total_pages = 0

    brands = {b.brand for b in all_prods} #set comprehension
    # print(brands)
    try:
      obj = paginator.get_page(page)
      total_pages = obj.paginator.num_pages
    except:
      obj = paginator.page(1)

    return render(request,'shop_headphones.html',{'objects':obj,'brands':brands,'pages':range(2,total_pages),'last_page':total_pages,'isFiltered':False,'isProductExist':True})

# Checkout Page
@login_required(login_url='login')
def checkout_page(request):

  cart_products = Cart.objects.filter(user=request.user)
  customer_addr = Customer.objects.filter(user=request.user)

  amount = 0.0
  shipping = 2.00
  last_total = 0.0

  for i in cart_products:
    amount += i.total_amount

  client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

  last_total = shipping + amount

  payment = client.order.create({'amount':last_total,'currency':'INR','payment_capture':1})

  print(payment)

  return render(request,'checkout.html',{'cart_products':cart_products,'customer_info':customer_addr,'total_amount':amount,'last_total':last_total,'razor_pay_total':last_total*100})

# Shop Pages
@login_required(login_url='login')
def orders_all_page(request):
  orders = OrderPlaced.objects.filter(user=request.user)
  total_amount = 0.0
  shipping = 2.0
  amount = 0.0

  for i in orders:
    amount += i.each_product_total_cost
  
  total_amount = shipping + amount

  past_orders = OrderPlaced.objects.filter(user=request.user).filter(order_status='Delivered').exists()

  if request.method == 'GET':
    cart = Cart.objects.filter(user=request.user)
    customer = Customer.objects.get(id=request.GET.get('customer_id'))
    payment_id = request.GET.get('payment_id')

    for item in cart:
      order = OrderPlaced(user=request.user,customer=customer,product=item.product,quantity=item.quantity,is_paid=True,razor_pay_payment_id=payment_id).save()
      product = Product.objects.get(product_name=item.product.product_name)
      product.product_quantity -= item.quantity
      product.save()
      item.delete()

    orders = OrderPlaced.objects.filter(user=request.user)

    total_amount = 0.0
    shipping = 2.0
    amount = 0.0

    for i in orders:
      amount += i.each_product_total_cost
    
    total_amount = shipping + amount

    past_orders = OrderPlaced.objects.filter(user=request.user).filter(order_status='Delivered').exists()

  return render(request,'orders_all.html',{'orders':orders,'amount':amount,'total_amount':total_amount,'past_orders':past_orders})
  
@login_required(login_url='login')
def orders_page(request):
  orders = OrderPlaced.objects.filter(user=request.user)

  return render(request,'orders.html',{'orders':orders})

def privacy_page(request):
  return render(request,'privacy_policy.html')

def signup_page(request):
   
  if request.method == 'POST':

    form = CustomerRegistrationForm(request.POST)
    # print(request.POST)

    if form.is_valid():
      # print('success')
      messages.success(request,'Congratulations!! Registered Successfully...')
      form.save()
    
    else:
      messages.error(request,form.errors)
  else:
    form = CustomerRegistrationForm(request.POST)


  return render(request,'register.html',{'form':form})

def login_page(request):

  msg = ""

  if request.method == 'POST':

    username = request.POST['username']
    password = request.POST['password']

    user_auth = authenticate(request,username=username,password=password)

    if user_auth is not None:
      login(request,user_auth)
      msg = "success"   

    else:
      msg = 'error'

  else:
    pass
  
  return render(request,'login.html',{'msg':msg})

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                # Update session to prevent the user from being logged out
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
            else:
                messages.error(request, 'Your old password was incorrect.')
        else:
            messages.error(request, 'There was an error with your submission. Please correct the errors below.')
    else:
        form = ChangePasswordForm()
    return render(request, 'changePassword.html', {'form': form})

@login_required(login_url='login')
def logout_page(request):
  logout(request)
  return redirect('home')

@login_required(login_url='login')
def invoice_pdf(request,payment_id):

  # customer_info = Customer.objects.get(id=customer_id)
  order = OrderPlaced.objects.filter(Q(user=request.user) & Q(razor_pay_payment_id=payment_id))

  total_amount = 0.0
  for i in order:
    total_amount += i.each_product_total_cost

  # print(order[0].customer)

  # return redirect('orders')

  order_details = {
    'order_id' : payment_id,
    'order_date' : order[0].ordered_date,
    'customer_name' : order[0].customer.customer_name,
    'address' : order[0].customer.customer_address + ' , ' + order[0].customer.customer_city + ' , ' + order[0].customer.customer_state,
    'items' : [item for item in order],
    'total' : total_amount + 50.00
  }

  # print(order_details.get('items'))
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = f'attachment; filename="invoice_{order_details['order_id'] }.pdf"'

  p = canvas.Canvas(response, pagesize=letter)
  width, height = letter

  # Set font styles
  p.setFont("Helvetica-Bold", 20)
  # Company Name
  p.setFillColor(colors.red)
  p.drawString(160, height - 35, "SHOPIFY E-COMMERCE")

  p.setFont("Helvetica-Bold", 16)
  # Header
  p.setFillColor(colors.blue)
  p.drawString(30, height - 55, "INVOICE OF PURCHASING")
  p.setFont("Helvetica", 12)
  p.setFillColor(colors.black)
  p.drawString(30, height - 70, f"Order ID: {order_details['order_id']}")
  p.drawString(30, height - 87, f"Ordered Date: {order_details['order_date']}")
  p.drawString(30, height - 105, f"Customer Name: {order_details['customer_name']}")
  p.drawString(30, height - 125, f"Address: {order_details['address']}")

  # Draw horizontal line
  p.line(30, height - 140, width - 30, height - 140)
  p.setFont("Helvetica-Bold", 12)
  # Table headers
  p.drawString(30, height - 160, "Product Name")
  p.drawString(200, height - 160, "Quantity")
  p.drawString(300, height - 160, "Price")
  p.drawString(400, height - 160, "Total")

  # Draw horizontal line
  p.line(30, height - 180, width - 30, height - 180)
  p.setFont("Helvetica", 12)

  y = height - 200
  for item in order_details['items']:
      p.drawString(30, y, item.product.product_name)
      p.drawString(200, y, str(item.quantity))
      p.drawString(300, y, f"${item.product.discounted_price:.2f}")
      p.drawString(400, y, f"${item.each_product_total_cost:.2f}")
      y -= 20

  # Draw horizontal line
  p.line(30, y - 10, width - 30, y - 10)

  # Total
  p.setFont("Helvetica-Bold", 13)
  # p.setFillColor(colors.red)
  p.drawString(300, y - 30, "Total:")
  p.drawString(400, y - 30, f"${order_details['total']:.2f}")
  p.setFont("Helvetica-Bold", 10)
  p.setFillColor(colors.black)
  p.drawString(390, y - 45, "(Taxes and Shipping are Included...)")

  p.showPage()
  p.save()

  return response

def cancelled_order(request,cancel_id):
  cancel_order = OrderPlaced.objects.get(id=cancel_id)
  cancel_order.order_status = 'Cancel'
  cancel_order.save()

  return redirect('orders')

# for admin panel
def admin_login_page(request):      

  if not request.user.is_superuser:

    msg = False
    err = False
    info = None

    if request.method == 'POST':

      username = request.POST.get('username')
      password = request.POST.get('password')

      form = authenticate(request,username=username,password=password)
      
      if form is not None:

        user = User.objects.get(username=username).is_superuser

        # print(user)

        if user:
          login(request,form)
          msg = True
          err = False
          info = 'Welcome To Admin Dashboard.'
      
        else:
          msg = True
          err = True
          info = 'Sorry,This Page is only for administrator.Not allowed any other users.'

      else:

        msg = True
        err = True
        info = 'Your Username or Password May be Wrong.Please Try Again.'

    return render(request,'admin_panel/login.html',{'msg':msg,'err':err,'info':info})

  else:
    return redirect('admin_dashboard')

def admin_dashboard(request):

  if request.user.is_superuser:
    orders = OrderPlaced.objects.all()
    customers = Customer.objects.all()

    total_revenue = 0.0
    total_products = len(orders)
    total_customers = len(customers)

    for i in orders:
      total_revenue += i.each_product_total_cost

    pedning_orders = orders.filter(order_status='Pending').count()

    return render(request,'admin_panel/dashboard.html',{'total_revenue':total_revenue,'total_products':total_products,'total_customers':total_customers,'pedning_orders':pedning_orders,'order_records':orders})

  else:
    return redirect('admin_login')

def admin_product(request):
  if request.user.is_superuser:

    msg = False

    if request.method == 'POST':
      form = ProductForm(request.POST, request.FILES)
      if form.is_valid():
          product = form.save(commit=False)
          product.save()
          form.save_m2m()  # Save the many-to-many data for the form.
          msg = True
    else:
        form = ProductForm()
    # return render(request, 'products/add_product.html', {'form': form})
    return render(request,'admin_panel/products.html',{'msg':msg,'form':form})

  else:
    return redirect('admin_login')

def admin_customers(request):
  if request.user.is_superuser:
    customer_list = Customer.objects.all()

    return render(request,'admin_panel/customers.html',{'customer_list':customer_list})

  else:
    return redirect('admin_login')

def admin_show_products(request):
  if request.user.is_superuser:
    prods = Product.objects.all().order_by('auto_increment_id')
    pagination = Paginator(prods,5)
    pages = request.GET.get('prod_page')
    pages_obj = pagination.get_page(pages)
    total_pages = pages_obj.paginator.num_pages
    return render(request,'admin_panel/show_products.html',{'page_obj':pages_obj,'pages':range(2,total_pages),'last_page':total_pages})

def admin_delete_product(request):
  if request.method == 'GET':      
      p_id = request.GET.get('prod')
      prod = Product.objects.get(id=p_id).delete()
      return JsonResponse({'status':'success'}) 
  return redirect('admin_show_products')