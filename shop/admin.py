from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


class GalleryInLine(admin.TabularInline):
    """Класс для загрузки фотографии в админке товара"""
    fk_name = 'product'
    model = models.Gallery
    extra = 1


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка админки для категорий"""
    list_display = ('title', 'parent', 'get_product_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_product_count(self, obj):
        """Возвращает кол-во товаров в категории"""
        if obj.product:
            return str(len(obj.product.all()))
        else:
            return 0

    # Даем название поля в админке
    get_product_count.short_description = 'Количество товаров'


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка админки для товара"""
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'size', 'color', 'get_photo')
    list_editable = ('price', 'quantity', 'size', 'color')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price')
    list_display_links = ('pk', 'title')
    inlines = (GalleryInLine,)

    def get_photo(self, obj):
        """Возвращает миниатюру товара"""
        if obj.images.all():
            return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
        else:
            return '-'

    # Даем название поля в админке
    get_photo.short_description = 'Миниатюра'


@admin.register(models.Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Настройка админки для галлереи"""
    list_display = ('image', 'get_photo')

    def get_photo(self, obj):
        """Возвращает миниатюру товара"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="65">')
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'
