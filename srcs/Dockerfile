# Utiliser une image Python comme base
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

RUN mkdir -p /app/backend
#- >/app/backend

# Copier les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --no-cache-dir -r ./tools/requirements.txt

RUN mkdir -p /var/www /var/www/static /var/www/media /var/www/media/avatars

COPY ./tools/run_server.sh /app/
COPY ./tools/default-avatar.jpg /var/www/media/avatars

RUN chmod +x /app/run_server.sh

EXPOSE 8000

WORKDIR /app/backend  
#- >/app/backend

ENTRYPOINT ["sh", "/app/run_server.sh"]
