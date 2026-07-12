from rest_framework import serializers

from .models import Brand, CarModel, Complaint, ComplaintPhoto, SiteSettings


class CarModelSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CarModel
        fields = [
            'id', 'brand', 'name', 'template_code', 'car_type', 'driver_cut',
            'package', 'second_row_package', 'notes', 'video_url', 'sheet_row',
        ]


class BrandSerializer(serializers.ModelSerializer):
    car_model_count = serializers.IntegerField(source='car_models.count', read_only=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'car_model_count']


class ComplaintPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintPhoto
        fields = ['id', 'image']


class ImageListField(serializers.ListField):
    child = serializers.ImageField()


class ComplaintSerializer(serializers.ModelSerializer):
    photos = ComplaintPhotoSerializer(many=True, read_only=True)
    uploaded_photos = ImageListField(write_only=True, required=False)

    class Meta:
        model = Complaint
        fields = [
            'id', 'car_model', 'name', 'phone', 'text', 'status',
            'created_at', 'photos', 'uploaded_photos',
        ]
        read_only_fields = ['status', 'created_at']

    def create(self, validated_data):
        photos = validated_data.pop('uploaded_photos', [])
        complaint = Complaint.objects.create(**validated_data)
        ComplaintPhoto.objects.bulk_create(
            ComplaintPhoto(complaint=complaint, image=image) for image in photos
        )
        return complaint


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            'address', 'latitude', 'longitude', 'about',
            'instagram_url', 'telegram_url', 'whatsapp_url',
        ]
