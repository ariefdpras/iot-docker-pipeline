FROM python:3.11-slim

# Set timezone ke Asia/Jakarta agar log sesuai dengan waktu lokal
ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code dan .env
COPY src/ ./src/
COPY .env .

# Bikin folder data di dalam container
RUN mkdir -p /app/data

# Command untuk run script
CMD ["python", "src/main.py"]
