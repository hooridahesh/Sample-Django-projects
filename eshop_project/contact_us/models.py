from django.db import models


# Create your models here.


class ContactUs(models.Model):
    title = models.CharField(max_length=300)
    email = models.EmailField(max_length=300)
    full_name = models.CharField(max_length=300)
    message = models.TextField()
    response = models.TextField(null=True, blank=True)
    is_read_by_admin = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'contact us'
        verbose_name_plural = 'contact us list'

    def __str__(self):
        return self.title


class profilemodel(models.Model):
    image = models.FileField(upload_to="images")
    """
    عکس ها و فایل ها مستقیم توی دیتابیس ذخیره نمیشن بلکه ادرسشون ذخیره میشه اونجا
    و خود فایل و عکس ها توی یه مکان فیزیکی ذخیره میشن که توی settings ادرس اصلی رو دادیم
    وبعد برای اون ادرس یه ساب فولدر به اسم images بعدا درست میشه
    """
