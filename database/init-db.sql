-- -- init-db.sql

-- -- #création de la base dédiée à notre projet
-- CREATE DATABASE '$POSTGRES_DB';

-- -- #création d'un nouvel utilisateur
-- CREATE USER '$POSTGRES_USER' WITH PASSWORD 'POSTGRES_PASSWORD' IF NOT EXISTS;

-- -- #on précise que l'encoding par défaut de notre utilisateur sera de l'utf8
-- ALTER ROLE '$POSTGRES_USER' SET client_encoding TO 'utf8';

-- -- #recommandation de django pour configurer notre base de données
-- ALTER ROLE '$POSTGRES_USER' SET default_transaction_isolation TO 'read committed';
-- ALTER ROLE '$POSTGRES_USER' SET timezone TO 'UTC';

-- -- #accorde les droits à notre nouvel utilisateur sur notre nouvelle base de données
-- GRANT ALL PRIVILEGES ON DATABASE '$POSTGRES_DB' TO '$POSTGRES_USER';

-- -- #permet à notre nouvel utilisateur de créer un nouveau schéma. Utile si vous voulez exécuter des tests
-- ALTER USER '$POSTGRES_USER' CREATEDB;

-- -- #création d'un schéma pour notre projet

