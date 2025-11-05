FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m eco

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . /app/
RUN chown -R eco:eco /app

USER eco

EXPOSE 8800

# Use entrypoint script to decide between development or production
ENTRYPOINT ["/entrypoint.sh"]
