# Быстрый старт

## 1. Установка зависимостей

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Создание базы данных

```bash
python manage.py migrate
```

## 3. Создание администратора

```bash
python manage.py createsuperuser
```

Введите:
- Username: admin
- Email: (опционально)
- Password: (ваш пароль)

**Важно:** Убедитесь, что пользователь имеет флаг `is_staff=True` (это устанавливается автоматически при создании через `createsuperuser`).

## 4. Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## 5. Тестирование API

### Вход в систему

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

Ответ:
```json
{
  "token": "your_token_here",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "",
    "is_staff": true
  }
}
```

### Создание категории

```bash
curl -X POST http://127.0.0.1:8000/api/categories/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Электроника",
    "is_active": true
  }'
```

### Создание товара

```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Смартфон",
    "category": 1,
    "description": "Современный смартфон",
    "price": "29999.00",
    "quantity": 10,
    "is_active": true
  }'
```

## Доступ к админ-панели Django

Откройте в браузере: http://127.0.0.1:8000/admin/

Войдите с учетными данными администратора, созданными на шаге 3.

