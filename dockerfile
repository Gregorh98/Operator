# Use lightweight Python image (good for Raspberry Pi too)
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    gcc \
    g++ \
    libportaudio2 \
    libatomic1 \
    libasound2-dev \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

RUN echo "defaults.pcm.card 2" > /root/.asoundrc && \
    echo "defaults.pcm.device 0" >> /root/.asoundrc && \
    echo "defaults.pcm.type plug" >> /root/.asoundrc

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /src .

CMD ["python", "main.py"]