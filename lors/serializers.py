from rest_framework import serializers

from .models import (
    Brand, CarModel, Color, Contact, Lead, LeadPhoto, Material, MatSetPrice, Page, Product,
    ProductCategory, ProductVariant, Review, SiteSettings,
)


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class MatSetPriceSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)

    class Meta:
        model = MatSetPrice
        fields = ['material', 'price']


class CarModelSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    mat_prices = MatSetPriceSerializer(source='mat_set_prices', many=True, read_only=True)

    class Meta:
        model = CarModel
        fields = [
            'id', 'brand', 'name', 'template_code', 'car_type', 'driver_cut',
            'package', 'second_row_package', 'notes', 'video_url', 'sheet_row', 'mat_prices',
        ]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']


class ProductVariantSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'color', 'price', 'image']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'variants']


class BrandSerializer(serializers.ModelSerializer):
    car_model_count = serializers.IntegerField(source='car_models.count', read_only=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'car_model_count']


class LeadPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadPhoto
        fields = ['id', 'image']


class ImageListField(serializers.ListField):
    child = serializers.ImageField()


class LeadSerializer(serializers.ModelSerializer):
    photos = LeadPhotoSerializer(many=True, read_only=True)
    uploaded_photos = ImageListField(write_only=True, required=False)

    class Meta:
        model = Lead
        fields = [
            'id', 'lead_type', 'name', 'phone', 'text', 'status', 'created_at',
            'car_model', 'material', 'mat_color', 'border_color', 'heel_color', 'product_variant',
            'photos', 'uploaded_photos',
        ]
        read_only_fields = ['status', 'created_at']

    def validate(self, attrs):
        lead_type = attrs.get('lead_type', Lead.TYPE_COMPLAINT)
        if lead_type == Lead.TYPE_COMPLAINT and not attrs.get('text'):
            raise serializers.ValidationError({'text': 'Обязательно для жалобы.'})
        if lead_type == Lead.TYPE_MAT_ORDER and not (attrs.get('car_model') and attrs.get('material')):
            raise serializers.ValidationError({'car_model': 'Модель авто и материал обязательны для заказа коврика.'})
        if lead_type == Lead.TYPE_PRODUCT_ORDER and not attrs.get('product_variant'):
            raise serializers.ValidationError({'product_variant': 'Обязателен для заказа товара.'})
        return attrs

    def create(self, validated_data):
        photos = validated_data.pop('uploaded_photos', [])
        lead = Lead.objects.create(**validated_data)
        LeadPhoto.objects.bulk_create(
            LeadPhoto(lead=lead, image=image) for image in photos
        )
        return lead


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'text', 'rating', 'source', 'photo', 'created_at']
        read_only_fields = ['source', 'created_at']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'contact_type', 'label', 'value']


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['slug', 'title', 'body', 'image', 'updated_at']


class SiteSettingsSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = SiteSettings
        fields = ['address', 'latitude', 'longitude', 'about', 'contacts']
