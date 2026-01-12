from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Max
from .models import (
    Category, Product, ProductPhoto, ProductTab,
    Filter, FilterValue
)
from .serializers import (
    CategorySerializer, CategoryListSerializer,
    ProductSerializer, ProductListSerializer,
    ProductPhotoSerializer, ProductTabSerializer,
    FilterSerializer, FilterValueSerializer,
    UserSerializer
)
from .permissions import IsAdminUser


class CustomAuthToken(ObtainAuthToken):
    """Кастомная аутентификация с проверкой прав администратора"""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Проверка, что пользователь является администратором
        if not user.is_staff:
            return Response(
                {'error': 'Доступ разрешен только администраторам'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({
            'token': token.key,
            'user': user_serializer.data
        })


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для категорий"""
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Включить/выключить категорию"""
        category = self.get_object()
        category.is_active = not category.is_active
        category.save()
        serializer = self.get_serializer(category)
        return Response(serializer.data)


class FilterViewSet(viewsets.ModelViewSet):
    """ViewSet для фильтров"""
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Filter.objects.all()
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class FilterValueViewSet(viewsets.ModelViewSet):
    """ViewSet для значений фильтров"""
    queryset = FilterValue.objects.all()
    serializer_class = FilterValueSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = FilterValue.objects.all()
        filter_id = self.request.query_params.get('filter', None)
        if filter_id:
            queryset = queryset.filter(filter_id=filter_id)
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet для товаров"""
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('category').prefetch_related(
            'photos', 'tabs', 'filter_values'
        )
        category_id = self.request.query_params.get('category', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Включить/выключить товар"""
        product = self.get_object()
        product.is_active = not product.is_active
        product.save()
        serializer = self.get_serializer(product)
        return Response(serializer.data)


class ProductPhotoViewSet(viewsets.ModelViewSet):
    """ViewSet для фото товаров"""
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = ProductPhoto.objects.all()
        product_id = self.request.query_params.get('product', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset.order_by('order', 'created_at')

    @action(detail=True, methods=['post'])
    def set_main(self, request, pk=None):
        """Установить главное фото"""
        photo = self.get_object()
        
        # Убираем главное фото у всех остальных фото этого товара
        ProductPhoto.objects.filter(
            product=photo.product
        ).exclude(id=photo.id).update(is_main=False)
        
        # Устанавливаем главное фото
        photo.is_main = True
        photo.save()
        
        serializer = self.get_serializer(photo)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """Изменить порядок фото"""
        photo_orders = request.data.get('orders', [])
        # Формат: [{'id': 1, 'order': 0}, {'id': 2, 'order': 1}, ...]
        
        with transaction.atomic():
            for item in photo_orders:
                photo_id = item.get('id')
                new_order = item.get('order')
                if photo_id and new_order is not None:
                    ProductPhoto.objects.filter(id=photo_id).update(order=new_order)
        
        return Response({'success': True})

    def perform_create(self, serializer):
        """Создание фото с автоматическим определением порядка"""
        product = serializer.validated_data.get('product')
        if not product:
            serializer.save()
            return
        
        # Если это первое фото, делаем его главным
        if not product.photos.exists():
            serializer.save(is_main=True)
        else:
            # Определяем максимальный порядок
            max_order = product.photos.aggregate(
                max_order=Max('order')
            )['max_order'] or 0
            serializer.save(order=max_order + 1)


class ProductTabViewSet(viewsets.ModelViewSet):
    """ViewSet для вкладок товаров"""
    queryset = ProductTab.objects.all()
    serializer_class = ProductTabSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = ProductTab.objects.all()
        product_id = self.request.query_params.get('product', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset.order_by('order', 'created_at')

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """Изменить порядок вкладок"""
        tab_orders = request.data.get('orders', [])
        # Формат: [{'id': 1, 'order': 0}, {'id': 2, 'order': 1}, ...]
        
        with transaction.atomic():
            for item in tab_orders:
                tab_id = item.get('id')
                new_order = item.get('order')
                if tab_id and new_order is not None:
                    ProductTab.objects.filter(id=tab_id).update(order=new_order)
        
        return Response({'success': True})

    def perform_create(self, serializer):
        """Создание вкладки с автоматическим определением порядка"""
        product = serializer.validated_data.get('product')
        if not product:
            serializer.save()
            return
        
        # Определяем максимальный порядок
        max_order = product.tabs.aggregate(
            max_order=Max('order')
        )['max_order'] or 0
        serializer.save(order=max_order + 1)
