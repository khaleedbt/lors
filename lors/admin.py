from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import Brand, CarModel, Complaint, ComplaintPhoto, Review, SiteSettings


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
    list_display = ['name', 'brand', 'template_code', 'car_type']
    list_filter = ['brand']
    search_fields = ['name', 'template_code']
    autocomplete_fields = ['brand']
    fieldsets = (
        (None, {'fields': ('brand', 'name')}),
        ('Шаблон и характеристики', {
            'fields': ('template_code', 'car_type', 'driver_cut', 'package', 'second_row_package'),
        }),
        ('Дополнительно', {'fields': ('notes', 'video_url', 'sheet_row')}),
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


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('Геолокация', {'fields': ('address', 'latitude', 'longitude')}),
        ('О компании', {'fields': ('about',)}),
        ('Соцсети', {'fields': ('instagram_url', 'telegram_url', 'whatsapp_url')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
