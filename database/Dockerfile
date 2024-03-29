# Utilisez une image de base PostgreSQL
FROM postgres:13

# Copiez le fichier SQL dans le conteneur
COPY init-db.sql /docker-entrypoint-initdb.d/

# Exécutez le script SQL lors du démarrage du conteneur
CMD ["postgres"]

