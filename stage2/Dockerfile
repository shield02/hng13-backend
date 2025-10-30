# ====================================
# Stage 1 - Build Dependencies
# ====================================
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ====================================
# Stage 2 - Runtime Image
# ====================================
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

ENV FLASK_APP=wsgi.py FLASK_ENV=production

# Ensure logs output correctly
ENV PYTHONUNBUFFERED=1

# Gunicorn for production
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "wsgi:app"]
