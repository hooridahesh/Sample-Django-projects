from django.db import models
from account.models import user
from product.models import product


# Create your models here.

class order(models.Model):  # این سبد خرید میشه
    user = models.ForeignKey(user, on_delete=models.CASCADE, verbose_name='کاربر')
    # این سبد خرید مال چه کاربری است
    is_paid = models.BooleanField(verbose_name='نهایی شده/نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    # برای این null , blank داره چون موقعی که پرداخت کرد تاریخ براش ثبت میشه نه موقعی که سبد خرید داشت
    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'

    def __str__(self):
        return self.user


class orderDetail(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    # این محصول برای کدوم سبد خریده
    product = models.ForeignKey(product, on_delete=models.CASCADE, verbose_name='محصول')
    # کدوم محصول رو دارم به سبد خرید اضافه میکنیم
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی محصول')
    # موقعی که پرداخت کردیم قیمت محصول ذخیره میشه
    count = models.IntegerField(verbose_name='تعداد')

    def get_total_price(self):
        return self.count * self.product.price

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'لیست جزئیات سبدهای خرید'

    def __str__(self):
        return self.order
