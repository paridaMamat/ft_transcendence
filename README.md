# ft_transcendence

## ft_start
### Configuration

Créez un fichier `.env` à la racine du projet en vous basant sur l'exemple fourni dans `.env.example`. Ce fichier contiendra les variables d'environnement nécessaires au bon fonctionnement du projet.

### Démarrage du Projet

Utilisez la commande suivante pour exécuter le projet :

```bash
make
```

Cette commande lancera les conteneurs Docker nécessaires et configurera l'environnement pour vous.

Accédez au site web à l'adresse [https://localhost:4000/](https://localhost:4000/) et à l'API à [https://localhost:8080/](https://localhost:8080/).

### Utilisation

Le projet utilise le framework `Django` pour le backend, la bibliothèque `React` pour le frontend et une base de données `PostgreSQL`.

Si vous avez besoin d'exécuter des commandes Django spécifiques sans les installer localement, vous pouvez utiliser la commande suivante :

```bash
docker exec -it <container_id> bash
```

Remplacez `<container_id>` par l'ID du conteneur Django, que vous pouvez obtenir en utilisant la commande :

```bash
docker ps
```