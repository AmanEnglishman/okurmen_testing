# Инструкция по деплою на сервер

## Подготовка

### Что нужно на сервере:

✅ **Только Docker и Docker Compose** - все остальное (Python, PostgreSQL, nginx, зависимости) установится автоматически в контейнерах

### Шаги подготовки:

1. **Скопируйте проект на сервер** `45.10.41.250` (через git, scp, rsync и т.д.)

2. **Создайте файл `.env`** на основе примера:
   ```bash
   cp env.example .env
   # или
   cp .env.example .env  # если файл называется .env.example
   ```

3. **Отредактируйте `.env` файл** и установите:
   - `SECRET_KEY` - сгенерируйте новый секретный ключ (можно использовать: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG=False` - для production
   - `DB_PASSWORD` - установите надежный пароль для PostgreSQL
   - `ALLOWED_HOSTS` - добавьте домен или IP сервера (45.10.41.250)
   - `CORS_ALLOWED_ORIGINS` - укажите домены фронтенда (если есть)

## Установка Docker и Docker Compose

**На сервере нужно установить только Docker и Docker Compose.** Все остальное (Python, PostgreSQL, nginx) будет установлено автоматически в контейнерах.

### Проверка установки

Сначала проверьте, установлены ли Docker и Docker Compose:

```bash
docker --version
docker compose version
```

### Установка Docker и Docker Compose

Если Docker не установлен на сервере, выберите один из способов:

#### Способ 1: Через apt (рекомендуется для Ubuntu/Debian)

```bash
# Обновить список пакетов
sudo apt update

# Установить необходимые пакеты
sudo apt install -y ca-certificates curl gnupg lsb-release

# Добавить официальный GPG ключ Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Добавить репозиторий Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установить Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Добавить пользователя в группу docker (чтобы не использовать sudo)
sudo usermod -aG docker $USER
# Выйти и зайти заново, чтобы изменения вступили в силу
```

#### Способ 2: Через snap (для Ubuntu)

```bash
# Установить Docker через snap
sudo snap install docker

# Добавить пользователя в группу docker
sudo addgroup --system docker
sudo adduser $USER docker
newgrp docker
```

#### Способ 3: Через официальный скрипт (универсальный)

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER
# Выйти и зайти заново
```

**Примечание:** 
- В новых версиях Docker используется `docker compose` (с пробелом), в старых - `docker-compose` (с дефисом)
- Если установлен через apt с `docker-compose-plugin`, используйте `docker compose`
- Если установлен старый docker-compose отдельно, используйте `docker-compose`
- В проекте используется `docker-compose.yml`, что работает с обоими вариантами

## Запуск приложения

**Примечание:** Используйте `docker compose` (с пробелом) если установлен через apt с плагином, или `docker-compose` (с дефисом) если установлен старый вариант.

1. Соберите и запустите контейнеры:
   ```bash
   # Новый вариант (docker compose)
   docker compose up -d --build
   
   # Или старый вариант (docker-compose)
   docker-compose up -d --build
   ```

2. Создайте суперпользователя Django:
   ```bash
   docker compose exec web python manage.py createsuperuser
   # или
   docker-compose exec web python manage.py createsuperuser
   ```

3. Проверьте логи:
   ```bash
   docker compose logs -f
   # или
   docker-compose logs -f
   ```

## Обслуживание

- Остановить контейнеры: `docker compose down` или `docker-compose down`
- Перезапустить: `docker compose restart` или `docker-compose restart`
- Просмотр логов: `docker compose logs -f web` или `docker-compose logs -f web`
- Выполнить миграции: `docker compose exec web python manage.py migrate` или `docker-compose exec web python manage.py migrate`
- Собрать статические файлы: `docker compose exec web python manage.py collectstatic` или `docker-compose exec web python manage.py collectstatic`

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

