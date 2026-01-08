from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Категория товаров с поддержкой подкатегорий"""
    name = models.CharField(max_length=200, verbose_name='Название')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent == self:
            raise ValidationError('Категория не может быть родителем самой себя')


class Filter(models.Model):
    """Фильтр для категорий"""
    name = models.CharField(max_length=200, verbose_name='Название фильтра')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='filters',
        verbose_name='Категория'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'
        ordering = ['name']
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class FilterValue(models.Model):
    """Значение фильтра"""
    filter = models.ForeignKey(
        Filter,
        on_delete=models.CASCADE,
        related_name='values',
        verbose_name='Фильтр'
    )
    value = models.CharField(max_length=200, verbose_name='Значение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Значение фильтра'
        verbose_name_plural = 'Значения фильтров'
        ordering = ['value']
        unique_together = ['filter', 'value']

    def __str__(self):
        return f"{self.filter.name}: {self.value}"


class Product(models.Model):
    """Товар"""
    name = models.CharField(max_length=200, verbose_name='Название')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Старая цена'
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    filter_values = models.ManyToManyField(
        FilterValue,
        related_name='products',
        blank=True,
        verbose_name='Значения фильтров'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        """Количество товара в наличии"""
        return self.quantity

    @property
    def out_of_stock(self):
        """Количество товара не в наличии (всегда 0, так как quantity показывает наличие)"""
        return 0

    def clean(self):
        if not self.name:
            raise ValidationError('Товар должен иметь название')
        if self.price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        if self.old_price and self.old_price < 0:
            raise ValidationError('Старая цена не может быть отрицательной')


class ProductPhoto(models.Model):
    """Фото товара"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Товар'
    )
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    is_main = models.BooleanField(default=False, verbose_name='Главное фото')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Фото {self.product.name}"

    def clean(self):
        if self.image:
            if self.image.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('Размер изображения не должен превышать 5MB')


class ProductTab(models.Model):
    """Вкладка товара (Описание, Характеристики и т.д.)"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='tabs',
        verbose_name='Товар'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    class Meta:
        verbose_name = 'Вкладка товара'
        verbose_name_plural = 'Вкладки товаров'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.title} ({self.product.name})"
