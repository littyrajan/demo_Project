from django.db.models import Q
from django.shortcuts import render
from django.utils.text import normalize_newlines

from shop.models import Product


# Create your views here.

def search_products(request):
    p=None
    query=""
    if (request.method == "POST"):
        query = request.POST['q']
        if query:
            p = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'search_products.html', {'p':p,'query':query})