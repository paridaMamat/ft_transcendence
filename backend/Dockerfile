
# Utiliser une image Python comme base
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copier les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances
RUN apt-get update && apt-get install -y postgresql-client
RUN apt-get install gettext -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./tools/requirements.txt

#RUN mkdir -p /var/www /var/www/static /var/www/media /var/www/media/avatars

COPY ./tools/run_server.sh /usr/src/app/
#COPY ./tools/default-avatar.jpg /var/www/media/avatars

RUN chmod +x /usr/src/app/run_server.sh

# Exposer le port sur lequel Django sera accessible
EXPOSE 8000

# Lancer l'application Django
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] && ["python", "manage.py", "migrate"] && ["python", "manage.py", "createsuperuser"]
ENTRYPOINT ["bash", "/app/tools/run_server.sh"]
