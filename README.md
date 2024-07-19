# Transcendence
ft_transcendence est le dernier projet du Tronc Coommun de 42 Paris.
Il a pour objectif de créer un site hébergeant le légendaire jeu Pong !

## Partie Obligatoire
### Jeu
- Créer un jeu Pong multi-joueur avec possibilité de jouer en tournoi.
- Le jeu doit pouvoir se jouer sur le même ordinateur, avec le même clavier. 

### SPA
- Le site doit être une Single Page Application (SPA) : pas de rechargement des pages coté serveur

## Modules Complémentaires
Possibilité d'ajouter des modules pour compléter l'expérience utilisateur, de jeu ou encore renforcer la sécurite du site.

### Un nouvel adversaire intelligent !
Nous avons codé un jeu Pong contre une AI.

### Vers plus de réalisme !
Les jeux Pong ont été développés en 3D avec la librairie ThreeJs.

### Encore plus de jeux !
Nous avons ajouté un second jeu, se jouant aussi en duel, le Memory Card.

### Une expérience utilisateur dynamisée
- Possibilité de jouer en partie simple ou de créer un tournoi.
- Conservation des données de jeu et statistiques personnelles consultables sur la page profil.
- Possibilité d'ajouter et/ou supprimer des amis.

### Authentification à distance
Inscription de l'utilisateur avec ses données de compte intra 42 pour les étudiants de l'école, avec l'API 42.

### Plus de sécurité
Configuration d'une authentification automatique avec JWT (Jason Web Token) et d'une authentification choisie, à deux facteurs. 

## Les langages utilisés
42 nous imposait des langages et frameworks spécifiques.

### Backend
Pour le Backend, nous avions le choix entre Ruby ou le framwork python Django.
Nous avons opté pour Django : opportunité d'utiliser un framework pour la 1e fois de notre cursus.
L'API Rest nous a servi pour les échanges entre le Front et la base de données : sérialization, CRUD, APIView..

### Base de Données
Plus performant pour les tableaux relationnels, PostGres a été préféré à SQLite3 (configurée par defaut dans Django).

### Frontend
Le Front a été développé en JS Vanilla, ainsi que la SPA et les jeux, implémentés coté client.
Bootstrap toolkit nous a servi pour le design, facilitant la manipulation de CSS. 
**NB: Interdiction d'utiliser les frameworks Java Script pour ce projet !**

### Docker
Configuration de l'architecture du projet en conteneurisation.

## Pour lancer le jeu
Complétez le fichier .env avec vos propres données et lancez le Makefile.

## Demo
![pong_vs](https://github.com/user-attachments/assets/f2ab458e-11a3-47df-bf50-c9bd252bc124)
![pong_AI](https://github.com/user-attachments/assets/bc058aa3-4b17-4468-bbc5-0665dc083237)
![memory_game](https://github.com/user-attachments/assets/f3b60faa-eded-4826-ada3-7b8a47e3f98c)
![friends_page](https://github.com/user-attachments/assets/8aebea38-a08f-47f7-9c63-5967fbb97c71)
![profil_page](https://github.com/user-attachments/assets/6da47fc1-65e4-4e4a-8aef-e3e8901d2056)

## Authors

* **Imen Mraoui** - [Imraoui](https://github.com/imenecole42)
* **Marine Vicedo** - [mvicedo](https://github.com/marine-vicedo)
* **Parida Maimaiti** - [pmaimait](https://github.com/paridaMamat)
* **Hinda Ferjani** - [hferjani](https://github.com/madamehinda)
* **Barbara Lefebvre** - [blefebvr](https://github.com/Barbara-LBV)

