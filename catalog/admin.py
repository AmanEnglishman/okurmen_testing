from django.contrib import admin
from .models import (
    Category, Product, ProductPhoto, ProductTab,
    Filter, FilterValue
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    list_editable = ['is_active']


class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 1
    fields = ['image', 'is_main', 'order']


class ProductTabInline(admin.TabularInline):
    model = ProductTab
    extra = 1
    fields = ['title', 'content', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price', 'old_price',
        'quantity', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    filter_horizontal = ['filter_values']
    inlines = [ProductPhotoInline, ProductTabInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'description', 'is_active')
        }),
        ('Цена и количество', {
            'fields': ('price', 'old_price', 'quantity')
        }),
        ('Фильтры', {
            'fields': ('filter_values',)
        }),
    )


@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_main', 'order', 'created_at']
    list_filter = ['is_main', 'created_at']
    list_editable = ['is_main', 'order']


@admin.register(ProductTab)
class ProductTabAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'order', 'created_at']
    list_filter = ['created_at']
    list_editable = ['order']


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name']


@admin.register(FilterValue)
class FilterValueAdmin(admin.ModelAdmin):
    list_display = ['filter', 'value', 'created_at']
    list_filter = ['filter', 'created_at']
    search_fields = ['value']
