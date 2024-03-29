-- init-db.sql
CREATE USER test WITH LOGIN PASSWORD '1234';
CREATE DATABASE ft_transcendence;
GRANT ALL PRIVILEGES ON DATABASE ft_transcendence TO test;
