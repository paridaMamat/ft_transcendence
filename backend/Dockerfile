
# Utiliser une image Python comme base
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copier les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances
RUN apt-get update && apt-get install -y postgresql-client
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


### Utiliser une image Python comme base
##FROM python:3.10

### Définir le répertoire de travail dans le conteneur
##WORKDIR /usr/src/app

### Installer les dépendances nécessaires
##RUN apt-get update && apt-get install -y nodejs npm postgresql-client

### Copier les fichiers backend et tools dans le conteneur
##COPY backend/ /usr/src/app/backend/
##COPY tools/ /usr/src/app/tools/

### Installer les dépendances Python
##RUN pip install --no-cache-dir -r /usr/src/app/tools/requirements.txt

### Copier les fichiers frontend dans le conteneur
##COPY website/ /usr/src/app/website/
##COPY ./website/package.json /usr/src/app/website/

### Changer le répertoire de travail pour le website
##WORKDIR /usr/src/app/website

### Installer les dépendances npm
##RUN npm install

### Installer webpack-bundle-tracker
##RUN npm install webpack-bundle-tracker --save-dev

### Construire les fichiers avec Webpack
##RUN npm run build

### Revenir au répertoire de travail principal
##WORKDIR /usr/src/app

### Rendre le script exécutable
##RUN chmod +x /usr/src/app/tools/run_server.sh

### Exposer le port sur lequel Django sera accessible
##EXPOSE 8000

### Lancer l'application Django
##ENTRYPOINT ["bash", "/usr/src/app/tools/run_server.sh"]

## Utiliser une image Python comme base
#FROM python:3.10

## Définir le répertoire de travail dans le conteneur
#WORKDIR /usr/src/app

## Copier les fichiers du projet dans le conteneur
#COPY . .

## Installer les dépendances
#RUN apt-get update && apt-get install -y postgresql-client
##RUN apt-get update && apt-get install -y nodejs npm postgresql-client
## Copier les fichiers backend et tools dans le conteneur
#COPY backend/ /usr/src/app/backend/
#COPY tools/ /usr/src/app/tools/
#RUN pip install --no-cache-dir -r ./tools/requirements.txt
##RUN mkdir -p /var/www /var/www/static /var/www/media /var/www/media/avatars

## Copier les fichiers frontend dans le conteneur
#COPY website/ /usr/src/app/website/
#COPY website/static /usr/src/app/website/static
#COPY ./website/package.json /usr/src/app/website/
#COPY ./tools/run_server.sh /usr/src/app/

## Changer le répertoire de travail pour le website
#WORKDIR /usr/src/app/website
## Installer webpack-bundle-tracker
##RUN npm install webpack-bundle-tracker --save-dev
## Construire les fichiers avec Webpack
##RUN npm run build

##COPY ./tools/default-avatar.jpg /var/www/media/avatars
#WORKDIR /usr/src/app

#RUN chmod +x /usr/src/app/run_server.sh

## Exposer le port sur lequel Django sera accessible
#EXPOSE 8000

## Lancer l'application Django
##CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] && ["python", "manage.py", "migrate"] && ["python", "manage.py", "createsuperuser"]
#ENTRYPOINT ["bash", "/app/tools/run_server.sh"]
