from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Brand, CarModel, Color, Complaint, Contact, ComplaintPhoto, Material, MatSetPrice, Page, Product,
    ProductCategory, ProductVariant, Review, SiteSettings,
)


class CarModelInline(TabularInline):
    model = CarModel
    extra = 0
    fields = ['name', 'template_code', 'car_type', 'driver_cut', 'package']
    show_change_link = True


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ['name', 'car_model_count']
    search_fields = ['name']
    inlines = [CarModelInline]

    @admin.display(description='моделей')
    def car_model_count(self, obj):
        return obj.car_models.count()


class MatSetPriceInline(TabularInline):
    model = MatSetPrice
    extra = 0
    fields = ['material', 'price']
    autocomplete_fields = ['material']


@admin.register(CarModel)
class CarModelAdmin(ModelAdmin):
    list_display = ['name', 'brand', 'template_code', 'car_type']
    list_filter = ['brand']
    search_fields = ['name', 'template_code']
    autocomplete_fields = ['brand']
    inlines = [MatSetPriceInline]
    fieldsets = (
        (None, {'fields': ('brand', 'name')}),
        ('Шаблон и характеристики', {
            'fields': ('template_code', 'car_type', 'driver_cut', 'package', 'second_row_package'),
        }),
        ('Дополнительно', {'fields': ('notes', 'video_url', 'sheet_row')}),
    )


@admin.register(Material)
class MaterialAdmin(ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']


@admin.register(Color)
class ColorAdmin(ModelAdmin):
    list_display = ['name', 'swatch', 'hex_code', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']

    @admin.display(description='')
    def swatch(self, obj):
        if not obj.hex_code:
            return ''
        return format_html(
            '<span style="display:inline-block;width:16px;height:16px;border-radius:3px;'
            'background:{};border:1px solid #999;"></span>', obj.hex_code,
        )


@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    search_fields = ['name']


class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 0
    fields = ['size', 'color', 'price', 'image', 'preview', 'is_active', 'order']
    readonly_fields = ['preview']
    autocomplete_fields = ['color']

    @admin.display(description='превью')
    def preview(self, obj):
        if not obj.image:
            return ''
        return format_html('<img src="{}" style="max-height: 80px;">', obj.image.url)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    autocomplete_fields = ['category']
    inlines = [ProductVariantInline]
    fieldsets = (
        (None, {'fields': ('category', 'name', 'description')}),
        ('Публикация', {'fields': ('is_active', 'order')}),
    )


class ComplaintPhotoInline(TabularInline):
    model = ComplaintPhoto
    extra = 0
    fields = ['image', 'preview']
    readonly_fields = ['preview']

    @admin.display(description='превью')
    def preview(self, obj):
        if not obj.image:
            return ''
        return format_html('<img src="{}" style="max-height: 120px;">', obj.image.url)


@admin.register(Complaint)
class ComplaintAdmin(ModelAdmin):
    list_display = ['name', 'phone', 'car_model', 'status', 'created_at']
    list_filter = ['status', 'car_model__brand']
    list_editable = ['status']
    search_fields = ['name', 'phone', 'text']
    autocomplete_fields = ['car_model']
    inlines = [ComplaintPhotoInline]
    readonly_fields = ['created_at']
    fieldsets = (
        ('Заявитель', {'fields': ('name', 'phone')}),
        ('Жалоба', {'fields': ('car_model', 'text', 'status')}),
        ('Служебное', {'fields': ('created_at',)}),
    )


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ['name', 'is_published', 'created_at', 'preview']
    list_filter = ['is_published']
    list_editable = ['is_published']
    search_fields = ['name', 'text']
    readonly_fields = ['preview', 'created_at']
    fieldsets = (
        (None, {'fields': ('name', 'text')}),
        ('Фото', {'fields': ('photo', 'preview')}),
        ('Публикация', {'fields': ('is_published', 'created_at')}),
    )

    @admin.display(description='превью')
    def preview(self, obj):
        if not obj.photo:
            return ''
        return format_html('<img src="{}" style="max-height: 120px;">', obj.photo.url)


@admin.register(Page)
class PageAdmin(ModelAdmin):
    list_display = ['title', 'slug', 'updated_at']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['updated_at']
    fieldsets = (
        (None, {'fields': ('slug', 'title')}),
        ('Содержимое', {'fields': ('body', 'image')}),
        ('Служебное', {'fields': ('updated_at',)}),
    )


class ContactInline(TabularInline):
    model = Contact
    extra = 0
    fields = ['contact_type', 'label', 'value', 'order']


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('Геолокация', {'fields': ('address', 'latitude', 'longitude')}),
        ('О компании', {'fields': ('about',)}),
    )
    inlines = [ContactInline]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
