"""python_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

# sarebbe meglio importarle nominativamente
# from . import views
from .views import home_page, about_page, contact_page

# per gli static files
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView

from carts.views import cart_home

from accounts.views import login_page, register_page

from django.contrib.auth.views import LogoutView

from accounts.views import guest_register_view

from addresses.views  import checkout_address_create_view

# from products.views import (
#     ProductListView, 
#     product_list_view, 
#     ProductDetailView, 
#     ProductDetailSlugView,
#     product_detail_view,
#     ProductFeaturedListView,
#     ProductFeaturedDetailView,
# )


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_page, name="home"),
    path('about/', about_page, name="about"),
    path('contact/', contact_page, name="contact"),
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html')),

    path('', include("products.urls", namespace='products')), #spostato nell altro urls
    # con namespace da il nome a tutto iò che è dentro include
    # che dovrà essere richaimato con namespace: url name speicfico

#     path('products/', ProductListView.as_view()), #spostato nell altro urls
#     path('products-fbv/', product_list_view),

# # posso chiamarli id o pk a mio piacimento
#     # path('products/<int:pk>', ProductDetailView.as_view()),
#     path('products/<str:slug>', ProductDetailSlugView.as_view()),
#     path('products-fbv/<int:pk>', product_detail_view),

#     path('featured/', ProductFeaturedListView.as_view()),
#     path('featured/<int:pk>', ProductFeaturedDetailView.as_view()),

    path('', include("search.urls", namespace='search')),

    # path('cart/', cart_home, name="cart"),
    path('cart/', include("carts.urls", namespace="cart")),

    # path('', include("carts.urls", namespace='carts')),

    path("logout/", LogoutView.as_view(), name="logout"),

    path('register/guest/', guest_register_view, name="guest_register"),

    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'), 
    
]

# setup e serve local e media files - python ecomemrce
# per gli static files
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)