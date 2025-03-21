# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Geckodriver (версия 0.36.0)
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.36.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.36.0-linux64.tar.gz

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код в контейнер
COPY . .

# Команда для запуска скрипта
CMD ["python", "your_script_name.py"]