from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from product.models import product
from django.http import HttpRequest, JsonResponse, HttpResponse
from .models import order, orderDetail
from django.shortcuts import redirect
import requests
import json
import time

# Create your views here.


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify_payment/'


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
    total = current_order.calculate_total_price()
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
    total = current_order.calculate_total_price()
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
    total = current_order.calculate_total_price()
    context = {
        'order': current_order,
        'sum': total
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('order/user_basket_content.html', context)
    })


def request_payment(request: HttpRequest):  # این کاربر رو به درگاه پرداخت انتقال میده
    current_order, created = order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total = current_order.calculate_total_price()
    if total == 0:
        return redirect(reverse('user_basket'))
    req_data = {
        "merchant_id": MERCHANT,
        "amount": total * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify_payment(request: HttpRequest):
    """
    بازگشت کاربر از درگاه پرداخت و نتیجه پرداخت کاربر هم بررسی میشه
    """
    current_order, created = order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total = current_order.calculate_total_price()
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                current_order.is_paid = True
                current_order.payment_date = time.time()
                current_order.save()
                ref_str = req.json()['data']['ref_id']
                return render(request, 'order/payment_result.html', {
                    'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد'
                })
            elif t_status == 101:
                return render(request, 'order/payment_result.html', {
                    'info': 'این تراکنش قبلا ثبت شده است'
                })
            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request, 'order/payment_result.html', {
                    'error': str(req.json()['data']['message'])
                })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            return render(request, 'order/payment_result.html', {
                'error': e_message
            })
    else:
        return render(request, 'order/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
        })
