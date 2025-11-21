from django.contrib import admin
from . import models


# Register your models here.

# class productAdmin(admin.ModelAdmin):
#     prepopulated_fields = {
#         'slug': ['title']
#     }
#     list_display = ['__str__', 'price', 'rating', 'is_active', 'category']
#     list_filter = ['rating', 'is_active']
#     list_editable = ['rating', 'is_active']

class productAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['price', 'is_active']


admin.site.register(models.product, productAdmin)
admin.site.register(models.productCategory)
admin.site.register(models.productTag)
admin.site.register(models.productBrand)
