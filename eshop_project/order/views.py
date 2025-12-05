from django.shortcuts import render
from django.template.loader import render_to_string

from product.models import product
from django.http import HttpRequest, JsonResponse
from .models import order, orderDetail


# Create your views here.

def add_product_to_order(request):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نمی باشد',
            'confirm_button_text': 'مرسی از شما',
            'icon': 'warning'
        })

    if request.user.is_authenticated:
        Product = product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if Product is not None:
            current_order, created = order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            """
            میخوایم ببینیم وقتی که محصول وجود داشت یا سبد خریدی برای کاربر در حال حاضر فعاله یا نه
            اگر فعال نبود که is_paid=True میشد و اگر فعال بود برابره با False میشه ینی کاربر هنوز
            پرداخت نکرده که سبد خریدش خالی بشه و get_or_create خروجیش یه تاپله که هم یه ابجکت میده
            وهم یه بولین که این ابجکت اینه که اگر سبد خرید بود که هیچی اگر نبود بسازش پس current_order
            میشه سبد خرید
            """
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            """
            میخوایم ببینیم محصولی که اضافه میکنیم توی سبد خرید الان هست یا نیست
            """
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                new_order = orderDetail(count=count, product_id=product_id, order_id=current_order.id)
                new_order.save()
            return JsonResponse({
                'status': 'success',
                'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
                'confirm_button_text': 'باشه ممنونم',
                'icon': 'success'
            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
                'confirm_button_text': 'مرسییییی',
                'icon': 'error'
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبد خرید ابتدا می بایست وارد سایت شوید',
            'confirm_button_text': 'ورود به سایت',
            'icon': 'error'
        })


def user_basket(request):
    current_order, created = order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total = 0
    for order_detail in current_order.orderdetail_set.all():
        total += order_detail.count * order_detail.product.price
    context = {
        'order': current_order,
        'sum': total
    }
    return render(request, 'order/user_basket.html', context)


def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })
    deleted_count, deleted_dict = orderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                             order__user_id=request.user.id).delete()
    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })
    current_order, created = order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total = 0
    for order_detail in current_order.orderdetail_set.all():
        total += order_detail.count * order_detail.product.price
    context = {
        'order': current_order,
        'sum': total
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('order/user_basket_content.html', context)
    })


def change_order_detail_count(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_state'
        })
    order_detail = orderDetail.objects.filter(id=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })
    current_order, created = order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total = 0
    for order_detail in current_order.orderdetail_set.all():
        total += order_detail.count * order_detail.product.price
    context = {
        'order': current_order,
        'sum': total
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('order/user_basket_content.html', context)
    })
