# Админ-панель интернет-магазина

Backend система для управления каталогом товаров интернет-магазина через админ-панель.

## Технологии

- Django 6.0.1
- Django REST Framework 3.16.1
- SQLite (база данных по умолчанию)

## Установка

1. Создайте виртуальное окружение (если еще не создано):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Выполните миграции:
```bash
python manage.py migrate
```

4. Создайте суперпользователя (администратора):
```bash
python manage.py createsuperuser
```

5. Запустите сервер:
```bash
python manage.py runserver
```

## API Endpoints

### Аутентификация

- **POST** `/api/auth/login/` - Вход в систему (только для администраторов)
  - Body: `{"username": "admin", "password": "password"}`
  - Response: `{"token": "...", "user": {...}}`

### Категории

- **GET** `/api/categories/` - Список категорий
- **POST** `/api/categories/` - Создать категорию
- **GET** `/api/categories/{id}/` - Детали категории
- **PUT/PATCH** `/api/categories/{id}/` - Обновить категорию
- **DELETE** `/api/categories/{id}/` - Удалить категорию
- **POST** `/api/categories/{id}/toggle_active/` - Включить/выключить категорию

### Товары

- **GET** `/api/products/` - Список товаров
  - Query params: `?category={id}`, `?is_active={true/false}`
- **POST** `/api/products/` - Создать товар
- **GET** `/api/products/{id}/` - Детали товара
- **PUT/PATCH** `/api/products/{id}/` - Обновить товар
- **DELETE** `/api/products/{id}/` - Удалить товар
- **POST** `/api/products/{id}/toggle_active/` - Включить/выключить товар

### Фото товаров

- **GET** `/api/product-photos/` - Список фото
  - Query params: `?product={id}`
- **POST** `/api/product-photos/` - Загрузить фото
- **GET** `/api/product-photos/{id}/` - Детали фото
- **PUT/PATCH** `/api/product-photos/{id}/` - Обновить фото
- **DELETE** `/api/product-photos/{id}/` - Удалить фото
- **POST** `/api/product-photos/{id}/set_main/` - Установить главное фото
- **POST** `/api/product-photos/reorder/` - Изменить порядок фото
  - Body: `{"orders": [{"id": 1, "order": 0}, {"id": 2, "order": 1}]}`

### Вкладки товаров

- **GET** `/api/product-tabs/` - Список вкладок
  - Query params: `?product={id}`
- **POST** `/api/product-tabs/` - Создать вкладку
- **GET** `/api/product-tabs/{id}/` - Детали вкладки
- **PUT/PATCH** `/api/product-tabs/{id}/` - Обновить вкладку
- **DELETE** `/api/product-tabs/{id}/` - Удалить вкладку
- **POST** `/api/product-tabs/reorder/` - Изменить порядок вкладок
  - Body: `{"orders": [{"id": 1, "order": 0}, {"id": 2, "order": 1}]}`

### Фильтры

- **GET** `/api/filters/` - Список фильтров
  - Query params: `?category={id}`
- **POST** `/api/filters/` - Создать фильтр
- **GET** `/api/filters/{id}/` - Детали фильтра
- **PUT/PATCH** `/api/filters/{id}/` - Обновить фильтр
- **DELETE** `/api/filters/{id}/` - Удалить фильтр

### Значения фильтров

- **GET** `/api/filter-values/` - Список значений
  - Query params: `?filter={id}`
- **POST** `/api/filter-values/` - Создать значение
- **GET** `/api/filter-values/{id}/` - Детали значения
- **PUT/PATCH** `/api/filter-values/{id}/` - Обновить значение
- **DELETE** `/api/filter-values/{id}/` - Удалить значение

## Аутентификация

Все API endpoints требуют аутентификации. Используйте токен, полученный при входе:

```
Authorization: Token <your_token>
```

## Валидации

- Товар не может быть сохранен без названия
- Цена не может быть отрицательной
- Старая цена не может быть отрицательной
- Размер фото ограничен 5MB
- Категория не может быть родителем самой себя

## Структура проекта

```
admin_panel/
├── admin_panel/          # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── catalog/              # Приложение каталога
│   ├── models.py        # Модели данных
│   ├── serializers.py   # Сериализаторы API
│   ├── views.py         # ViewSets для API
│   ├── urls.py          # URL маршруты
│   ├── admin.py         # Админ-панель Django
│   └── permissions.py   # Разрешения доступа
├── media/               # Загруженные файлы
├── manage.py
└── requirements.txt
```

## Использование

1. Войдите в систему через `/api/auth/login/` с учетными данными администратора
2. Используйте полученный токен для всех последующих запросов
3. Создайте категории через `/api/categories/`
4. Создайте фильтры для категорий через `/api/filters/`
5. Добавьте значения фильтров через `/api/filter-values/`
6. Создайте товары через `/api/products/`
7. Загрузите фото товаров через `/api/product-photos/`
8. Добавьте вкладки товаров через `/api/product-tabs/`

## Django Admin

Также доступна стандартная админ-панель Django по адресу `/admin/` для визуального управления данными.

