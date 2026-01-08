from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    CategoryViewSet, ProductViewSet, ProductPhotoViewSet,
    ProductTabViewSet, FilterViewSet, FilterValueViewSet,
    CustomAuthToken
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-photos', ProductPhotoViewSet, basename='product-photo')
router.register(r'product-tabs', ProductTabViewSet, basename='product-tab')
router.register(r'filters', FilterViewSet, basename='filter')
router.register(r'filter-values', FilterValueViewSet, basename='filter-value')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomAuthToken.as_view(), name='api_login'),
]

