from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('add-cart/<pizza_id>/', add_cart, name='add-cart'),
    path('cart/',cart,name='cart'),
    path('/', logout_user, name='logout'),
    path('order/',order,name='order'),
    path('remove_cart_item/<cart_item_uid>/', remove_cart_item, name='remove_cart_item')
]