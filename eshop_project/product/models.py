from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.

class productCategory(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان', db_index=True)
    url_title = models.CharField(max_length=300, verbose_name='عنوان در url', db_index=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField()

    def __str__(self):
        return f"{self.url_title}"

    class Meta:  # در واقع این کلاس برای کانفیگ کردن اطلاعات کلاس مورد نظر است
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'


class productBrand(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField()

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.title


class product(models.Model):
    title = models.CharField(max_length=300)
    brand = models.ForeignKey(productBrand, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ManyToManyField(productCategory, null=True, blank=True)
    """
    این cascade برای اینه که اگر ما بیایم جدول دسته بندی رو پاک کنیم
     محصول هایی هم که داره پاک بشه ینی مثلا ما دسته بندی گوشی داریم و
     این دسته بندی گوشی پاک میشه ولی محصول های سامسونگ یا ایفون یا.. هنوز هست
     پس اینا هم پاک میشه باهاش
    """
    price = models.IntegerField()
    image = models.ImageField(upload_to="images/product", blank=True, null=True)
    short_description = models.CharField(max_length=500, null=True, db_index=True)
    description = models.TextField(db_index=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField()
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, unique=True, max_length=200)

    # sumsung galaxy 4 => sumsung-galaxy-4
    """
         * default="" ینی اگر چیزی وارد نشه پیش فرضش رشته خالی باشه
         
         *null=False ینی این فیلد نباید خالی بمونه و دیتابیس نباید مقدار نال داشته باشه
         
         *وقتی db_index=True ینی وقتی به اسلاگ مورد نظر می رسیم به جای اینکه
          بره توی کل سطرها دنبال اون اسلاگ بگرده می ره توی اون فهرستی که براشون ایندکس درست شده می گرده
          ولی خیلی تند اون اسلاگ رو پیدا میکنه وگرنه اگر می خواست توی همه سطرها برگرده خیلی کند پیش می رفت
          و واسه اینکه از این اسلاگ زیاد استفاده می کنیم واسه همین براش db_index درست کردیم
          پس لازم نیست برای هر فیلد درست کنیم چون خود همین هم یه جا برای ذخیره شده می گیره
    """

    def __str__(self):
        return f"{self.title},({self.price})"

    def save(self, *args, **kwargs):  # این متد برای آپدیت کردن دیتابیس است
        """
        *در واقع اینجا این متد سیو رو اومدیم دوباره بازنویسی کردیم ینی هر وقت که محصول میخواد ذخیره بشه سلاگش از روی تایتل ساخته بشه

         *اون دوتا ارگومان توی ورودی باعث میشه که جنگو خطا نده
        ینی اگر این دوتا ارگومان رو نداشته باشیم چون تابع جدید با تابع اصلی سازگار نیست جنگو خطا میده پس 
        به صورت عمومی می نویسیم تابع رو که جنگو هر ارگومانی که می خواست بتونه بفرسته
        """
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        """ اینجا هم میگه برو نخسه اصلی سیو از کلاس والد رو صدا بزن و داده رو ذخیره کن"""

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class productTag(models.Model):
    Tag = models.CharField(max_length=300, db_index=True)
    product_tag = models.ForeignKey(product, on_delete=models.CASCADE)

    def __str__(self):
        return self.Tag

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
