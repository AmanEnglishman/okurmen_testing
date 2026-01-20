#!/bin/bash

# Скрипт для генерации self-signed SSL сертификатов для разработки

SSL_DIR="./nginx/ssl"
DAYS_VALID=365

# Создаем директорию для SSL сертификатов
mkdir -p "$SSL_DIR"

# Генерируем приватный ключ
echo "Генерация приватного ключа..."
openssl genrsa -out "$SSL_DIR/key.pem" 2048

# Генерируем самоподписанный сертификат
echo "Генерация самоподписанного сертификата..."
openssl req -new -x509 -key "$SSL_DIR/key.pem" -out "$SSL_DIR/cert.pem" -days $DAYS_VALID \
    -subj "/C=RU/ST=State/L=City/O=Organization/CN=localhost"

# Устанавливаем правильные права доступа
chmod 600 "$SSL_DIR/key.pem"
chmod 644 "$SSL_DIR/cert.pem"

echo "SSL сертификаты успешно созданы в $SSL_DIR"
echo "cert.pem - сертификат"
echo "key.pem - приватный ключ"
echo ""
echo "ВНИМАНИЕ: Это self-signed сертификат для разработки!"
echo "Для продакшена используйте Let's Encrypt (см. SSL_SETUP.md)"

