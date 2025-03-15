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
from tkinter.font import names

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from shop import views

app_name="shop"
urlpatterns = [
    path('', views.Categories, name='categories'),
    path('products/<int:id>', views.Products, name='products'),
    path('all_products',views.All_products,name='all_products'),
    path('single_product/<int:pk>',views.Single_Product,name='single_product'),
    path('404',views.Page404,name='404'),
    path('contact',views.Contact,name='contact'),
    path('about',views.About,name='about'),
    path('news',views.News,name='news'),
    path('single-news',views.Single_news,name='single-news'),
    path('register', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),
    path('add_stock/<int:pk>', views.Add_stock.as_view(), name='add_stock'),
    path('add_category', views.Add_category.as_view(), name='add_category'),
    path('add_product', views.Add_product.as_view(), name='add_product'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
