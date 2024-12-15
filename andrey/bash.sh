#!/bin/bash

# Убедитесь, что файл исполним:
# chmod +x run.sh

# Остановка и удаление старых контейнеров (если они есть)
echo "Остановка и удаление старых контейнеров..."
docker-compose down

# Сборка Docker-образа (если не используете docker-compose, замените на 'docker build')
echo "Сборка Docker-образа..."
docker-compose build

# Запуск контейнера (если не используете docker-compose, замените на 'docker run')
echo "Запуск контейнера..."
docker-compose up -d

# Логирование вывода контейнера
echo "Контейнер запущен. Логи контейнера:"
docker-compose logs -f
