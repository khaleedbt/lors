from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .filters import CarModelFilter
from .models import Brand, CarModel, Complaint, Review, SiteSettings
from .search import smart_search_car_models
from .serializers import (
    BrandSerializer, CarModelSerializer, ComplaintSerializer, ReviewSerializer, SiteSettingsSerializer,
)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filterset_fields = ['name']
    search_fields = ['name']


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='search', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                description=(
                    'Ищет по марке и модели. "Subaru" — все модели марки Subaru. '
                    '"Subaru XV" — конкретная модель, если такая есть в каталоге; '
                    'если нет — все модели марки Subaru.'
                ),
            ),
        ],
    ),
)
class CarModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarModel.objects.select_related('brand').all()
    serializer_class = CarModelSerializer
    filterset_class = CarModelFilter

    def get_queryset(self):
        search = self.request.query_params.get('search', '').strip()
        if not search:
            return super().get_queryset()
        return smart_search_car_models(search)


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


class ReviewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReviewSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Review.objects.all()
        if self.action == 'create':
            return qs
        return qs.filter(is_published=True)


class SiteSettingsView(generics.RetrieveAPIView):
    serializer_class = SiteSettingsSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return SiteSettings.load()
