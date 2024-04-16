# Utilisez une image de base PostgreSQL
FROM postgres:14

# Copiez le fichier SQL dans le conteneur
# init-db.sql est le fichier SQL qui contient les commandes pour créer la base de données et les tables
COPY init-db.sql /docker-entrypoint-initdb.d/

# Exécutez le script SQL lors du démarrage du conteneur
CMD ["postgres"]

