FROM selenium/standalone-firefox:latest

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY . .

# Run the script
CMD ["python", "your_script_name.py"]