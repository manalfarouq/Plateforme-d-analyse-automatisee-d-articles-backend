FROM python:3.11-slim

WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 8001

# Démarrer l'application
# Les variables d'environnement seront fournies au runtime via docker-compose ou -e
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]