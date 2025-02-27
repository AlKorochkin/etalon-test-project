FROM python:3.11-slim

# Установим системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /etalon-test-project

# Копируем только файлы зависимостей
COPY requirements.txt etalon-test-project/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . /etalon-test-project