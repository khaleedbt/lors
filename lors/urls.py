from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    BrandViewSet, CarModelViewSet, ColorViewSet, DeseOptionViewSet, LeadViewSet, LogoOptionViewSet,
    MaterialViewSet, PageViewSet, PriceCategoryViewSet, PricingSettingsView, ProductCategoryViewSet,
    ProductViewSet, ReviewViewSet, SiteSettingsView,
)

router = DefaultRouter()
router.register('brands', BrandViewSet)
router.register('car-models', CarModelViewSet)
router.register('leads', LeadViewSet, basename='lead')
router.register('reviews', ReviewViewSet, basename='review')
router.register('pages', PageViewSet, basename='page')
router.register('materials', MaterialViewSet, basename='material')
router.register('colors', ColorViewSet, basename='color')
router.register('price-categories', PriceCategoryViewSet, basename='price-category')
router.register('logo-options', LogoOptionViewSet, basename='logo-option')
router.register('dese-options', DeseOptionViewSet, basename='dese-option')
router.register('products', ProductViewSet, basename='product')
router.register('product-categories', ProductCategoryViewSet, basename='product-category')

urlpatterns = router.urls + [
    path('settings/', SiteSettingsView.as_view(), name='site-settings'),
    path('pricing-settings/', PricingSettingsView.as_view(), name='pricing-settings'),
]
