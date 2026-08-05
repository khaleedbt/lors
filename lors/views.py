from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from django.db.models import Prefetch

from .filters import CarModelFilter
from .models import (
    Brand, CarModel, Color, DeseOption, Lead, LogoOption, Material, Page, PriceCategory, PricingSettings,
    Product, ProductCategory, ProductVariant, Review, SiteSettings,
)
from .search import smart_search_car_models
from .serializers import (
    BrandSerializer, CarModelSerializer, ColorSerializer, DeseOptionSerializer, LeadSerializer,
    LogoOptionSerializer, MaterialSerializer, PageSerializer, PriceCategorySerializer, PricingSettingsSerializer,
    ProductCategorySerializer, ProductSerializer, ReviewSerializer, SiteSettingsSerializer,
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
    queryset = CarModel.objects.select_related('brand', 'price_category').all()
    serializer_class = CarModelSerializer
    filterset_class = CarModelFilter

    def get_queryset(self):
        search = self.request.query_params.get('search', '').strip()
        if not search:
            return super().get_queryset()
        return smart_search_car_models(search)


class LeadViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Lead.objects.select_related(
        'car_model__brand', 'car_model__price_category', 'material', 'mat_color', 'border_color', 'heel_color',
        'logo', 'dese', 'product_variant',
    ).prefetch_related('photos')
    serializer_class = LeadSerializer
    parser_classes = [MultiPartParser, FormParser]
    filterset_fields = ['status', 'lead_type', 'car_model']

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


class PriceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceCategory.objects.all()
    serializer_class = PriceCategorySerializer
    permission_classes = [permissions.AllowAny]


class LogoOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogoOption.objects.filter(is_active=True)
    serializer_class = LogoOptionSerializer
    permission_classes = [permissions.AllowAny]


class DeseOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeseOption.objects.filter(is_active=True)
    serializer_class = DeseOptionSerializer
    permission_classes = [permissions.AllowAny]


class PricingSettingsView(generics.RetrieveAPIView):
    serializer_class = PricingSettingsSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return PricingSettings.load()


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.filter(is_active=True)
    serializer_class = MaterialSerializer
    permission_classes = [permissions.AllowAny]


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.filter(is_active=True)
    serializer_class = ColorSerializer
    permission_classes = [permissions.AllowAny]


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related(
        Prefetch('variants', queryset=ProductVariant.objects.filter(is_active=True).select_related('color')),
    )
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['category']


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class SiteSettingsView(generics.RetrieveAPIView):
    serializer_class = SiteSettingsSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return SiteSettings.load()
