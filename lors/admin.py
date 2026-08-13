from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Brand, CarModel, Color, Contact, Lead, LeadPhoto, LogoOption, Material, Page, PriceCategory,
    Product, ProductCategory, ProductVariant, Review, SiteSettings,
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


@admin.register(CarModel)
class CarModelAdmin(ModelAdmin):
    list_display = ['name', 'brand', 'template_code', 'car_type', 'body_variant', 'year_from', 'year_to', 'price_category']
    list_filter = ['brand', 'car_type', 'price_category']
    search_fields = ['name', 'template_code', 'base_model']
    autocomplete_fields = ['brand', 'price_category']
    fieldsets = (
        (None, {'fields': ('brand', 'name')}),
        ('Шаблон и характеристики', {
            'fields': ('template_code', 'car_type', 'driver_cut', 'package', 'second_row_package'),
        }),
        ('Цена', {'fields': ('price_category',)}),
        ('Каскад Марка→Модель→Кузов→Год (авторазбор из названия)', {
            'fields': ('base_model', 'body_variant', 'year_from', 'year_to'),
        }),
        ('Дополнительно', {'fields': ('notes', 'video_url', 'sheet_row')}),
    )


@admin.register(PriceCategory)
class PriceCategoryAdmin(ModelAdmin):
    list_display = ['name', 'price', 'order', 'car_model_count']
    list_editable = ['price', 'order']
    search_fields = ['name']

    @admin.display(description='моделей')
    def car_model_count(self, obj):
        return obj.car_models.count()


@admin.register(LogoOption)
class LogoOptionAdmin(ModelAdmin):
    list_display = ['name', 'price', 'order', 'is_active']
    list_editable = ['price', 'order', 'is_active']
    search_fields = ['name']


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


@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display = ['product', 'size', 'color', 'price', 'is_active']
    list_filter = ['is_active', 'product__category']
    search_fields = ['product__name', 'size']
    autocomplete_fields = ['product', 'color']


class LeadPhotoInline(TabularInline):
    model = LeadPhoto
    extra = 0
    fields = ['image', 'preview']
    readonly_fields = ['preview']

    @admin.display(description='превью')
    def preview(self, obj):
        if not obj.image:
            return ''
        return format_html('<img src="{}" style="max-height: 120px;">', obj.image.url)


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ['name', 'phone', 'lead_type', 'car_model', 'status', 'created_at']
    list_filter = ['lead_type', 'status', 'car_model__brand']
    list_editable = ['status']
    search_fields = ['name', 'phone', 'text']
    autocomplete_fields = [
        'car_model', 'material', 'mat_color', 'border_color', 'heel_color', 'logo', 'product_variant',
    ]
    inlines = [LeadPhotoInline]
    readonly_fields = ['created_at']
    fieldsets = (
        ('Заявитель', {'fields': ('lead_type', 'name', 'phone', 'text', 'status')}),
        ('Заказ коврика', {
            'fields': (
                'car_model', 'material', 'mat_color', 'border_color', 'heel_color', 'logo',
            ),
        }),
        ('Заказ товара', {'fields': ('product_variant',)}),
        ('Служебное', {'fields': ('created_at',)}),
    )


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ['name', 'rating', 'source', 'is_published', 'created_at', 'preview']
    list_filter = ['is_published', 'source', 'rating']
    list_editable = ['is_published']
    search_fields = ['name', 'text']
    readonly_fields = ['preview', 'created_at']
    fieldsets = (
        (None, {'fields': ('name', 'text', 'rating', 'source')}),
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
