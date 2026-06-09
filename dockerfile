# Use lightweight Python image (good for Raspberry Pi too)
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

COPY /src .

CMD ["python", "main.py"]