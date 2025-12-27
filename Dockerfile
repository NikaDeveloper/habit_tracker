FROM python:3.13-slim

# Устанавливаем системные зависимости для работы с Postgres
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# проект использует pip-tools, копируем requirements.txt
# (Предварительно генерим его из .in файла командой pip-compile)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда для запуска (используем gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
