from django.shortcuts import render, get_object_or_404
from .models import product
from django.db.models import Avg
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView

# Create your views here.

# def product_list(request):
#     products = product.objects.all().order_by("-price")[:5]
#     # average_of_rating = products.aggregate(Avg("rating"))
#     return render(request, 'product/product_list.html', {
#         "products": products,
#     })


# def product_details(request, slug):
#     Product = get_object_or_404(product, slug=slug)
#     return render(request, 'product/product_detail.html', {'product': Product})

# ----------------------------------------------------------------------------#

# class productListView(TemplateView):
#     template_name = 'product/product_list.html'
#
#     def get_context_data(self, **kwargs):
#         products = product.objects.all().order_by("-price")[:5]
#         context = super(productListView, self).get_context_data()
#         context['products'] = products
#         return context

"""
خود جنگو یه بخشی داره که بهمون لیست از محصولات و.. رو نشون میده کلا برای نشان دادن لیسته
به جای اینکه بیایم مثل productListView عمل کنیم برای نشان دادن لیستی از محصولات می تونیم
مثل پایین پیش بریم
"""


class productListView(ListView):
    template_name = 'product/product_list.html'
    model = product
    context_object_name = 'products'

    def get_queryset(self):
        base_query = super(productListView, self).get_queryset()
        data = base_query.filter(is_active=True)
        return data


# class productDetailsView(TemplateView):
#     template_name = 'product/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(productDetailsView, self).get_context_data()
#         slug = kwargs['slug']
#         Product = get_object_or_404(product, slug=slug)
#         context['product'] = Product
#         return context

"""
برای اینکه جزئیات محصول رو نشون بدیم می تونیم از DetailView استفاده کنیم
این DetailView از slug می فهمه که باید کدوم محصول رو نشون بده
"""


class productDetailsView(DetailView):
    template_name = 'product/product_detail.html'
    model = product
    context_object_name = 'product_detail'
