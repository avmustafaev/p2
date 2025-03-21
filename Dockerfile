FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    xvfb \  # Virtual display for headless mode
    libgl1-mesa-glx \  # OpenGL library
    libgl1-mesa-dri \  # Direct Rendering Infrastructure
    libpci-dev \  # PCI utilities (required for GPU detection)
    && rm -rf /var/lib/apt/lists/*

# Install Geckodriver (version 0.36.0)
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.36.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.36.0-linux64.tar.gz

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY . .

# Run the script with xvfb
CMD ["xvfb-run", "python", "your_script_name.py"]