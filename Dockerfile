FROM python:3.11-slim

# Installer les dépendances système nécessaires (Chrome, Xvfb, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    unzip \
    chromium \
    chromium-driver \
    xvfb \
    fonts-liberation \
    python3-tk \
    python3-dev \
    inetutils-ping \
    && apt-get clean

# Créer le dossier de travail
WORKDIR /app

# Copier tous les fichiers dans le conteneur
COPY . /app

# Installer les dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Exposer le port Flask
EXPOSE 5000

# Utiliser xvfb-run pour démarrer Xvfb et exécuter Flask
CMD ["python", "app.py"]
