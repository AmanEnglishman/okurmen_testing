# Инструкция по деплою на сервер

## Подготовка

1. Скопируйте проект на сервер `45.10.41.250`
2. Создайте файл `.env` на основе примера:
   ```bash
   cp .env.example .env
   ```
3. Отредактируйте `.env` файл и установите:
   - `SECRET_KEY` - сгенерируйте новый секретный ключ
   - `DEBUG=False` - для production
   - `DB_PASSWORD` - установите надежный пароль для PostgreSQL
   - `ALLOWED_HOSTS` - добавьте домен или IP сервера

## Установка Docker и Docker Compose

Если Docker не установлен на сервере:

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Запуск приложения

1. Соберите и запустите контейнеры:
   ```bash
   docker-compose up -d --build
   ```

2. Создайте суперпользователя Django:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

3. Проверьте логи:
   ```bash
   docker-compose logs -f
   ```

## Обслуживание

- Остановить контейнеры: `docker-compose down`
- Перезапустить: `docker-compose restart`
- Просмотр логов: `docker-compose logs -f web`
- Выполнить миграции: `docker-compose exec web python manage.py migrate`
- Собрать статические файлы: `docker-compose exec web python manage.py collectstatic`

## Настройка SSL (опционально)

Для настройки HTTPS:

1. Получите SSL сертификаты (например, через Let's Encrypt)
2. Раскомментируйте секцию HTTPS в `nginx/nginx.conf`
3. Укажите пути к сертификатам
4. Перезапустите nginx: `docker-compose restart nginx`

## Структура

- `web` - Django приложение (порт 8000 внутри контейнера)
- `db` - PostgreSQL база данных (порт 5432)
- `nginx` - веб-сервер (порты 80 и 443)

Приложение будет доступно по адресу: `http://45.10.41.250`

