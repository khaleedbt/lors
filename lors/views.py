from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .filters import CarModelFilter
from .models import Brand, CarModel, Complaint, SiteSettings
from .serializers import BrandSerializer, CarModelSerializer, ComplaintSerializer, SiteSettingsSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filterset_fields = ['name']
    search_fields = ['name']


class CarModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarModel.objects.select_related('brand').all()
    serializer_class = CarModelSerializer
    filterset_class = CarModelFilter
    search_fields = ['name', 'template_code', 'brand__name']


class ComplaintViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Complaint.objects.select_related('car_model__brand').prefetch_related('photos')
    serializer_class = ComplaintSerializer
    parser_classes = [MultiPartParser, FormParser]
    filterset_fields = ['status', 'car_model']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class SiteSettingsView(generics.RetrieveAPIView):
    serializer_class = SiteSettingsSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return SiteSettings.load()
