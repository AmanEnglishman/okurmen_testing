from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Product, ProductPhoto, ProductTab,
    Filter, FilterValue
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории"""
    children = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'parent', 'is_active',
            'children', 'products_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_children(self, obj):
        """Получить дочерние категории"""
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True).data

    def get_products_count(self, obj):
        """Количество товаров в категории"""
        return obj.products.count()


class CategoryListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка категорий"""
    children_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'parent', 'is_active',
            'children_count', 'products_count', 'created_at', 'updated_at'
        ]

    def get_children_count(self, obj):
        return obj.children.count()

    def get_products_count(self, obj):
        return obj.products.count()


class FilterValueSerializer(serializers.ModelSerializer):
    """Сериализатор значения фильтра"""
    class Meta:
        model = FilterValue
        fields = ['id', 'value', 'created_at']
        read_only_fields = ['created_at']


class FilterSerializer(serializers.ModelSerializer):
    """Сериализатор фильтра"""
    values = FilterValueSerializer(many=True, read_only=True)

    class Meta:
        model = Filter
        fields = ['id', 'name', 'category', 'values', 'created_at']
        read_only_fields = ['created_at']


class ProductPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор фото товара"""
    class Meta:
        model = ProductPhoto
        fields = [
            'id', 'product', 'image', 'is_main', 'order', 'created_at'
        ]
        read_only_fields = ['created_at']

    def validate_image(self, value):
        """Проверка размера изображения"""
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError(
                'Размер изображения не должен превышать 5MB'
            )
        return value


class ProductTabSerializer(serializers.ModelSerializer):
    """Сериализатор вкладки товара"""
    class Meta:
        model = ProductTab
        fields = [
            'id', 'product', 'title', 'content', 'order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товара"""
    photos = ProductPhotoSerializer(many=True, read_only=True)
    tabs = ProductTabSerializer(many=True, read_only=True)
    filter_values = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=FilterValue.objects.all(),
        required=False
    )
    in_stock = serializers.ReadOnlyField()
    out_of_stock = serializers.ReadOnlyField()
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name', 'description',
            'price', 'old_price', 'quantity', 'in_stock', 'out_of_stock',
            'is_active', 'filter_values', 'photos', 'tabs',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_name(self, value):
        """Проверка названия товара"""
        if not value or not value.strip():
            raise serializers.ValidationError('Товар должен иметь название')
        return value.strip()

    def validate_price(self, value):
        """Проверка цены"""
        if value < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return value

    def validate_old_price(self, value):
        """Проверка старой цены"""
        if value is not None and value < 0:
            raise serializers.ValidationError(
                'Старая цена не может быть отрицательной'
            )
        return value


class ProductListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка товаров"""
    main_photo = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name',
            'price', 'old_price', 'quantity', 'is_active',
            'main_photo', 'created_at'
        ]

    def get_main_photo(self, obj):
        """Получить главное фото"""
        main_photo = obj.photos.filter(is_main=True).first()
        if main_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main_photo.image.url)
            return main_photo.image.url
        return None


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
        read_only_fields = ['is_staff']

