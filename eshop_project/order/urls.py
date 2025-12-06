from django.urls import path
from . import views

urlpatterns = [
    path('add_to_order', views.add_product_to_order, name='add_to_order'),
    path('user_basket', views.user_basket, name='user_basket'),
    path('remove_order_detail', views.remove_order_detail, name='remove_order_detail'),
    path('change_order_detail', views.change_order_detail_count, name='change_order_detail'),
    path('request_payment/', views.request_payment, name='request_payment'),
    path('verify_payment/', views.verify_payment, name='verify_payment')
]
