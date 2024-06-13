# Utiliser une image Python comme base
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copier les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gettext \
    libpq-dev

# Installer pip et les dépendances Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r./tools/requirements.txt

# Créer les répertoires nécessaires
RUN mkdir -p /var/www /var/www/static /var/www/media /var/www/media/avatars

# Copier les scripts et fichiers supplémentaires
COPY ./tools/run_server.sh /usr/src/app/
COPY ./tools/default-avatar.jpg /var/www/media/avatars

# Rendre le script exécutable
RUN chmod +x /usr/src/app/run_server.sh

# Exposer le port sur lequel Django sera accessible
EXPOSE 8000

# Lancer l'application Django
ENTRYPOINT ["bash", "/usr/src/app/run_server.sh"]