"""
URL configuration for Globegrid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from cart import views


app_name ="cart"

urlpatterns = [
    path('add_to_cart/<int:i>/', views.Add_to_cart,name="add_to_cart"),
    path('cart_view/', views.Cart_view,name="cart_view"),
    path('cart_decrement/<int:i>/',views.Cart_decrement,name="cart_decrement"),
    path('cart_delete/<int:i>/',views.Cart_delete,name="cart_delete"),
    path('billing_details/', views.Billing_details,name="billing_details"),
    path('status_payment<str:p>', views.Status_payment,name="status_payment"),
    path('orders', views.Orders,name="orders"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
