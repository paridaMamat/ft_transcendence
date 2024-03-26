#!/bin/bash
#set -eux

# log into MariaDB as root and create database and the user
psql -h localhost -U postgres -c "CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER}"
psql -h localhost -U postgres -c "CREATE USER  IF NOT EXIST ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}'"

## Attribution des privilèges à l'utilisateur
#psql -h localhost -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER}"

## Configuration du mot de passe de l'utilisateur root (à utiliser avec précaution)
#psql -h localhost -U postgres -c "ALTER USER postgres PASSWORD '${POSTGRES_ROOT_PASSWORD}'"

## Rechargement des privilèges pour que les modifications prennent effet
#psql -h localhost -U postgres -c "FLUSH PRIVILEGES;"

#print status
echo "PostGreSQL database and user were created successfully! "