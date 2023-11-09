# Utilizamos una imagen de Python con Debian como base
FROM python:3.10-slim

# Instalamos las dependencias necesarias para compilar dlib y face_recognition
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libboost-all-dev \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo en /app
WORKDIR /app

# Actualizamos pip e instalamos las dependencias del proyecto
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copiamos el código de tu proyecto a /app
COPY . .

# Comando de inicio para ejecutar tu aplicación Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
