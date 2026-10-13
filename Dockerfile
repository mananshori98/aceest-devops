FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py

WORKDIR /app

# curl is required by the HEALTHCHECK (not included in slim images)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies in their own layer for build-cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as a non-root user; /app/instance holds the SQLite database
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Initialise the database, then start the app
CMD ["sh", "-c", "flask init-db && flask run --host=0.0.0.0"]
