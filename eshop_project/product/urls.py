from django.urls import path
from . import views

urlpatterns = [
    # path('', views.product_list),
    # path('<slug:slug>', views.product_details, name='product_detail'),
    path('', views.productListView.as_view()),
    path('<slug:slug>', views.productDetailsView.as_view(), name='product_detail')
]
