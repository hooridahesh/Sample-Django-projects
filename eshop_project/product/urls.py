from django.urls import path
from . import views

urlpatterns = [
    # path('', views.product_list),
    # path('<slug:slug>', views.product_details, name='product_detail'),
    path('', views.productListView.as_view(), name='product_list'),
    path('cat/<cat>', views.productListView.as_view(), name='product_categories_list'),
    path('brand/<brand>', views.productListView.as_view(), name='product_brands_list'),
    path('<slug:slug>', views.productDetailsView.as_view(), name='product_detail')
]
