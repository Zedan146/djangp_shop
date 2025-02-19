from django.contrib import admin

from . import models


class GalleryInLine(admin.TabularInline):
    """Класс для загрузки фотографии в админки товара"""
    fk_name = 'product'
    model = models.Gallery
    extra = 1


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка админки для категорий"""
    list_display = ('title', 'parent', 'get_product_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_product_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка админки для товара"""
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'size', 'color')
    list_editable = ('price', 'quantity', 'size', 'color')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price')
    list_display_links = ('pk', 'title')
    inlines = (GalleryInLine,)


admin.site.register(models.Gallery)
