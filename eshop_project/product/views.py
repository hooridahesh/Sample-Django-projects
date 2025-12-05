from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from .models import product
from django.db.models import Avg, Count
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from .models import productCategory, productBrand

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
    paginate_by = 3
    """
    برای paging صفحه میباشد که میگه توی هر صفحه فقط یه ایتم رو نشون بده
    و این باعث میشه یکسری اطلاعات هم به صفحه html فرستاده بشه ینی یه چیزایی مثل paginator و..
    و می تونیم ازشون استفاده کنیم اونجا 
    """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(productListView, self).get_context_data()
        query = product.objects.all()
        Product: product = query.order_by('-price').first()
        db_max_price = Product.price if Product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        return context

    def get_queryset(self):
        query = super(productListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)
        if end_price is not None:
            query = query.filter(price__lte=end_price)
        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)

        return query


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


def product_categories_component(request):
    product_categories = productCategory.objects.filter(is_active=True, is_delete=False)
    return render(request, 'product/components/product_categories_component.html', {'categories': product_categories})


def product_brands_component(request):
    product_brands = productBrand.objects.annotate(product_counter=Count('product')).filter(is_active=True)
    """
    تابع annotate روی ابجکت اعمال میشه و میگه بیا اون دیتایی که میخوایی واکشی کن
    و چیزهای اضافیه هم که نیاز داری من برات میارم و روی سطر هم اعمال میشه
    """
    return render(request, 'product/components/product_brands_component.html', {'brands': product_brands})
