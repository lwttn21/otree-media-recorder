# Basis-Image: schlankes Python 3.11
FROM python:3.11-slim

# Verhindert debconf-Warnungen im Docker-Build
ENV DEBIAN_FRONTEND=noninteractive

# Arbeitsverzeichnis im Container
WORKDIR /app

# Systempakete installieren, die psycopg2 braucht
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Restliche Projektdateien kopieren
COPY . .

# WICHTIG:
# Rechte auf /app korrigieren, damit User 1000 oTree/SQLite UND Media-Recorder nutzen kann
RUN chown -R 1000:1000 /app

# Container läuft als derselbe User wie auf deinem Host (ubuntu = uid 1000)
USER 1000:1000

# Startbefehl beim Containerstart
CMD ["otree", "prodserver", "0.0.0.0:8000"]
