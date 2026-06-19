# Imagen para el proyecto Django "sigfrid"
FROM python:3.12-slim

# No generar .pyc y salida sin buffer (logs en tiempo real)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Dependencias de sistema:
#  - libpq5: cliente de PostgreSQL en tiempo de ejecucion (psycopg2)
#  - libjpeg/zlib: soporte de imagenes para Pillow
# Las wheels binarias ya incluyen casi todo, pero estas garantizan el runtime.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        libjpeg62-turbo \
        zlib1g \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias primero para aprovechar la cache de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del codigo (en desarrollo se sobreescribe con el volumen)
COPY . .

EXPOSE 8000

# El comando real lo define compose.yaml (migraciones + runserver).
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
