FROM selenium/standalone-firefox:latest

# Устанавливаем необходимые системные зависимости
USER root
RUN apt-get update && apt-get install -y \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Создаем виртуальное окружение
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт
COPY . .

# Запускаем скрипт
CMD ["python", "your_script_name.py"]