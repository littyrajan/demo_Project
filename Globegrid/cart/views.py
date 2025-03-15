import math
from decimal import *
from http.client import responses
from lib2to3.fixes.fix_input import context

import razorpay
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from shop.models import Product
from cart.models import CartPro,Order_detail,Payment


# Create your views here.

@login_required
def Cart_view(request):
    u = request.user
    c = CartPro.objects.filter(user=u)
    #to calculate Total
    total = 0
    for i in c:
        total += i.quantity * i.product.price
    tax = (Decimal(.13) * total)
    format_tax = "{:.2f}".format(tax)
    totalaftertax = total + tax
    shipping = math.ceil(totalaftertax) - totalaftertax
    format_shipping = "{:.2f}".format(shipping)
    amount = "{:.2f}".format(totalaftertax + shipping)

    print(amount)

    context = {'cart':c,'total':total,'tax':format_tax,'amount':amount,'shipping':format_shipping}
    return render(request,'cart.html', context)

@login_required
def Add_to_cart(request,i):
    p = Product.objects.get(id=i)
    u = request.user #userdetails
    try:   #if record already there
        c = CartPro.objects.get(user=u,product=p)
        if p.stock>0:
            c.quantity +=1  #update the record already inside table cart
            c.save()
            p.stock -= 1
            p.save()

    except:  #if no record present
        if p.stock:
            c = CartPro.objects.create(product=p, user=u, quantity=1)
            c.save()
            p.stock -= 1
            p.save()

    return redirect('cart:cart_view')


@login_required
def Cart_decrement(request,i):
    p = Product.objects.get(id=i)
    u = request.user #userdetails
    try:   #if record already there
        c = CartPro.objects.get(user=u,product=p)
        if c.quantity > 1:
            c.quantity -=1  #update the record already inside table cart
            c.save()
            p.stock += 1
            p.save()
        else:
            c.delete()
            p.stock += 1
            p.save()

    except:  # if no record present
        pass

    return redirect('cart:cart_view')

@login_required
def Cart_delete(request,i):
    p = Product.objects.get(id=i)
    u = request.user  # userdetails
    try:  # if record already there
        c = CartPro.objects.get(user=u, product=p)
        c.delete()
        p.stock += 1
        p.save()

    except:  # if no record present
        pass

    return redirect('cart:cart_view')


def Billing_details(request):
    u = request.user
    c = CartPro.objects.filter(user=u)
    # to calculate Total
    total = 0
    for i in c:
        total += i.quantity * i.product.price
    tax = (Decimal(.13) * total)
    format_tax = "{:.2f}".format(tax)
    totalaftertax = total + tax
    shipping = math.ceil(totalaftertax) - totalaftertax
    format_shipping = "{:.2f}".format(shipping)
    amount = "{:.2f}".format(totalaftertax + shipping)


    if (request.method == "POST"):
        street_address = request.POST['street_address']
        city = request.POST['city']
        province = request.POST['province']
        country = request.POST['country']
        postal_code = request.POST['postal_code']
        phone_number = request.POST['phone_number']

        #Razorpay client connection
        client = razorpay.Client(auth=('rzp_test_C8GC9hNjXCKJNG','22gOuI6RcZP1DT91CmciEQFh'))

        # Razorpay order creation
        response_payment = client.order.create(dict(amount=int(float(amount))*100,currency='CAD'))
        print("response_payment : ",response_payment)
        order_id = response_payment['id'] #retrieve order id from response
        status = response_payment['status'] #retrieve status from response

        if(status == "created"):
            p = Payment.objects.create(name = u.username,amount=int(float(amount)),order_id= order_id)
            p.save()
            for i in c:
                o = Order_detail.objects.create(product=i.product,user=i.user,street_address=street_address,city=city,province=province,country=country,postal_code=postal_code,phone_number=phone_number,order_id=order_id,no_of_items=i.quantity)
                o.save()
            context1 = {'payment':response_payment,'name':u.username}
            return render(request,'payment.html',context1)


    context = {'total':total,'tax':format_tax,'amount':amount,'shipping':format_shipping}
    return render(request, 'billing_details.html',context)


from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def Status_payment(request,p):
    user = User.objects.get(username = p)
    login(request, user)  #login back to same username after payment

    response = request.POST
    print("Response : ",response)  # razorpay response after successful

    #To check the validity(authenticity)
    param_dict = {
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    client = razorpay.Client(auth=('rzp_test_C8GC9hNjXCKJNG','22gOuI6RcZP1DT91CmciEQFh'))

    try:
        status = client.utility.verify_payment_signature(param_dict)
        print("Status : ",status)

        p = Payment.objects.get(order_id = response['razorpay_order_id'])
        p.paid = True
        p.razorpay_payment_id = response['razorpay_payment_id']
        p.save()

        o = Order_detail.objects.filter(order_id = response['razorpay_order_id'])
        for i in o:
            i.payment_status = "completed"
            i.save()

        c = CartPro.objects.filter(user=user)
        c.delete()

    except:
        pass



    return render(request,'status_payment.html')


def Orders(request):
    u = request.user
    o = Order_detail.objects.filter(user=u,payment_status="completed")
    contexto = {'orders':o}
    return render(request, 'orders.html',contexto)


