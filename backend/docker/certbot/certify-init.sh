#!/bin/sh

# Ожидает доступности прокси, затем получает первый сертификат.

set -e

# Используем netcat (nc) для проверки порта 80 и проверяем каждые 5 секунд.
# пока порт не станет доступен. Требуется, чтобы nginx успел запуститься раньше всех
# и сертификат-бот запускается.

until nc -z proxy 80; do
    echo "Waiting for proxy..."
    sleep 5s & wait ${!}
done

echo "Getting certificate..."

certbot certonly \
    --webroot \
    --webroot-path "/vol/www/" \
    -d "$DOMAIN" \
    --email $EMAIL \
    --rsa-key-size 4096 \
    --agree-tos \
    --noninteractive