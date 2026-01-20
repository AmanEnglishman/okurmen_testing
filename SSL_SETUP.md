# Настройка SSL для Docker

Этот документ описывает настройку SSL/TLS для проекта в Docker.

## Быстрый старт (Self-signed сертификаты для разработки)

Для локальной разработки можно использовать self-signed сертификаты:

1. Запустите скрипт генерации сертификатов:
```bash
./nginx/generate-ssl.sh
```

2. Запустите Docker Compose:
```bash
docker-compose up -d
```

3. Приложение будет доступно по HTTPS:
   - HTTP: `http://localhost` (автоматически перенаправляет на HTTPS)
   - HTTPS: `https://localhost`

**Важно:** Браузер покажет предупреждение о небезопасном соединении для self-signed сертификатов. Это нормально для разработки.

## Настройка для продакшена (Let's Encrypt)

Для продакшена рекомендуется использовать Let's Encrypt для получения бесплатных SSL сертификатов.

### Вариант 1: Использование certbot вручную

1. Убедитесь, что домен указывает на ваш сервер (DNS настроен правильно)

2. Временно отключите редирект на HTTPS в `nginx/nginx.conf`:
   - Закомментируйте блок `return 301 https://$host$request_uri;` в server блоке на порту 80

3. Запустите контейнеры:
```bash
docker-compose up -d
```

4. Установите certbot на хост-машине (если еще не установлен):
```bash
sudo apt-get update
sudo apt-get install certbot
```

5. Получите сертификат:
```bash
sudo certbot certonly --webroot -w ./nginx/certbot -d yourdomain.com -d www.yourdomain.com
```

6. Скопируйте сертификаты в директорию nginx/ssl:
```bash
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./nginx/ssl/key.pem
sudo chmod 644 ./nginx/ssl/cert.pem
sudo chmod 600 ./nginx/ssl/key.pem
```

7. Включите обратно редирект на HTTPS в `nginx/nginx.conf`

8. Перезапустите nginx:
```bash
docker-compose restart nginx
```

### Вариант 2: Автоматическое обновление с certbot в Docker

Можно добавить сервис certbot в `docker-compose.yml` для автоматического получения и обновления сертификатов.

1. Обновите `docker-compose.yml`, добавив сервис certbot (см. пример ниже)

2. Получите сертификат:
```bash
docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d yourdomain.com
```

3. Настройте автоматическое обновление через cron или systemd timer

## Структура директорий

```
nginx/
├── nginx.conf          # Конфигурация nginx с SSL
├── ssl/                # SSL сертификаты
│   ├── cert.pem        # Сертификат
│   └── key.pem         # Приватный ключ
├── certbot/            # Для Let's Encrypt (webroot)
└── generate-ssl.sh     # Скрипт генерации self-signed сертификатов
```

## Настройка Django для HTTPS

Убедитесь, что в `settings.py` включены настройки для работы через прокси:

```python
# settings.py
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Проверка SSL

После настройки проверьте SSL:

1. Откройте `https://yourdomain.com` в браузере
2. Проверьте сертификат через онлайн-инструменты:
   - https://www.ssllabs.com/ssltest/
   - https://sslchecker.com/

## Обновление сертификатов Let's Encrypt

Сертификаты Let's Encrypt действительны 90 дней. Для автоматического обновления:

```bash
# Добавьте в crontab (crontab -e):
0 0 1 * * cd /path/to/project && docker-compose run --rm certbot renew && docker-compose restart nginx
```

## Устранение проблем

### Ошибка: "SSL certificate not found"
- Убедитесь, что файлы `cert.pem` и `key.pem` существуют в `nginx/ssl/`
- Проверьте права доступа: `chmod 644 cert.pem` и `chmod 600 key.pem`

### Ошибка: "Permission denied"
- Убедитесь, что nginx контейнер имеет доступ к файлам сертификатов
- Проверьте, что директория `nginx/ssl` существует и монтируется правильно

### Браузер не принимает self-signed сертификат
- Это нормально для разработки. Нажмите "Продолжить" или "Advanced" → "Proceed to localhost"
- Для продакшена используйте Let's Encrypt

## Безопасность

- **Никогда не коммитьте приватные ключи в Git!**
- Добавьте `nginx/ssl/` в `.gitignore`
- Используйте сильные пароли и правильные права доступа к файлам
- Регулярно обновляйте сертификаты Let's Encrypt

