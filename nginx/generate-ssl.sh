#!/bin/bash

# Скрипт для генерации self-signed SSL сертификатов для работы с IP адресом

SSL_DIR="./nginx/ssl"
DAYS_VALID=365

# IP адрес (можно передать как аргумент или использовать по умолчанию)
IP_ADDRESS="${1:-45.10.41.250}"

echo "Генерация SSL сертификата для IP адреса: $IP_ADDRESS"

# Создаем директорию для SSL сертификатов
mkdir -p "$SSL_DIR"

# Создаем конфигурационный файл для OpenSSL с поддержкой IP адреса
CONFIG_FILE=$(mktemp)
cat > "$CONFIG_FILE" <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C=RU
ST=State
L=City
O=Organization
CN=$IP_ADDRESS

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
IP.1 = $IP_ADDRESS
IP.2 = 127.0.0.1
DNS.1 = localhost
EOF

# Генерируем приватный ключ
echo "Генерация приватного ключа..."
openssl genrsa -out "$SSL_DIR/key.pem" 2048

# Генерируем самоподписанный сертификат с поддержкой IP адреса
echo "Генерация самоподписанного сертификата..."
openssl req -new -x509 -key "$SSL_DIR/key.pem" -out "$SSL_DIR/cert.pem" -days $DAYS_VALID \
    -config "$CONFIG_FILE" -extensions v3_req

# Удаляем временный конфигурационный файл
rm "$CONFIG_FILE"

# Устанавливаем правильные права доступа
chmod 600 "$SSL_DIR/key.pem"
chmod 644 "$SSL_DIR/cert.pem"

echo ""
echo "✓ SSL сертификаты успешно созданы в $SSL_DIR"
echo "  - cert.pem - сертификат"
echo "  - key.pem - приватный ключ"
echo ""
echo "Сертификат действителен для:"
echo "  - IP: $IP_ADDRESS"
echo "  - IP: 127.0.0.1 (localhost)"
echo "  - DNS: localhost"
echo ""
echo "ВНИМАНИЕ: Это self-signed сертификат!"
echo "Браузер покажет предупреждение о безопасности - это нормально."
echo ""
echo "Использование:"
echo "  ./nginx/generate-ssl.sh [IP_ADDRESS]"
echo "  Пример: ./nginx/generate-ssl.sh 45.10.41.250"

