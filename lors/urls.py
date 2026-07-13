from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BrandViewSet, CarModelViewSet, ComplaintViewSet, ReviewViewSet, SiteSettingsView

router = DefaultRouter()
router.register('brands', BrandViewSet)
router.register('car-models', CarModelViewSet)
router.register('complaints', ComplaintViewSet, basename='complaint')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = router.urls + [
    path('settings/', SiteSettingsView.as_view(), name='site-settings'),
]
