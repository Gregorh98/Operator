# Use lightweight Python image (good for Raspberry Pi too)
FROM python:3.11-slim

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy project files into container
COPY . /app

# Install dependencies if you have a requirements file
RUN pip install --no-cache-dir -r requirements.txt || true

# Run the script
CMD ["python", "main.py"]