
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.base import kwarg_re
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from shop.models import Category

from shop.models import Product


# Create your views here.
def Categories(request):

    c = Category.objects.all()
    context = {'c':c}
    return render(request,'categories.html',context)

def Products(request,id):
    p=Product.objects.filter(Q(category_id=id))
    print(p)
    context = {'p':p}

    return render(request, 'products.html',context)

def All_products(request):
    p=Product.objects.all()
    c = Category.objects.all()

    return render(request, 'all_products.html',{'c': c,'p':p})

def Single_Product(request,pk):
    s = Product.objects.get(id=pk)
    context = {'Product': s}
    return render(request, 'single_product.html',context)

def Page404(request):
    return render(request,'404.html')

def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')

def News(request):
    return render(request,'news.html')

def Single_news(request):
    return render(request,'single-news.html')

def user_login(request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password = password)
        if user:
            login(request,user)
            return Categories(request)
        else:
            return HttpResponse("Invalid login")

    return render(request,'login.html')


def user_register(request):
    if(request.method=="POST"):
        u = request.POST['username']
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        e = request.POST['email']
        p = request.POST['password']
        p1 = request.POST['password1']

        if (p == p1):
            r = User.objects.create_user(username=u, first_name=fn, last_name=ln, email=e, password=p)
            r.save()
            return user_login(request)
        else:
            return HttpResponse("Passwords are not same")

    return render(request, 'register.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('shop:user_login')



class Add_stock(UpdateView):
    model = Product
    template_name = "add_stock.html"
    fields = ['stock']
    # success_url = reverse_lazy('shop:products')

    def get_success_url(self):
        return reverse_lazy('shop:single_product',kwargs={'pk':self.object.id})


class Add_product(CreateView):
    model = Product
    template_name = "add_product.html"
    fields = ['name','image','description','price','stock','available','category']
    success_url = reverse_lazy('shop:categories')


class Add_category(CreateView):
    model = Category
    template_name = "add_category.html"
    fields = ['name','image','description']
    success_url = reverse_lazy('shop:categories')



