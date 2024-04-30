#from django.urls import path, include
#from django.contrib.auth.models import User
#from website.models import CustomUser

#from rest_framework import serializers

#class UserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = CustomUser
#        fields = ['username', 'password']

"""
create() -> creer de nouveaux objets (nouveaux tableaux) : pas besoin
retrieve() -> GET HTTP pour recuperer un objet specifique

Dans Django REST Framework (DRF), les classes serializer sont utilisées pour convertir 
les objets Django en JSON et vice versa. Voici quelques-unes des classes serializer 
les plus couramment utilisées dans DRF :

1. **Serializer** : Cette classe de base est utilisée pour créer des sérialiseurs 
personnalisés. Vous pouvez étendre cette classe pour créer vos propres sérialiseurs.

2. **ModelSerializer** : C'est une classe de sérialiseur spéciale qui fournit une 
implémentation simple et concise pour la sérialisation et la désérialisation de 
modèles Django. Il simplifie la création de sérialiseurs pour vos modèles en générant 
automatiquement des champs basés sur les champs de votre modèle.

3. **HyperlinkedModelSerializer** : Cette classe de sérialiseur est similaire à 
ModelSerializer, mais elle utilise des hyperliens pour représenter les relations entre
les modèles plutôt que des clés étrangères.

4. **SerializerMethodField** : Ce champ spécial vous permet de définir des méthodes 
personnalisées dans votre sérialiseur pour calculer des valeurs dynamiques à inclure 
dans votre réponse JSON.

5. **PrimaryKeyRelatedField** : Ce champ permet de représenter les relations ManyToMany 
ou ForeignKey en utilisant simplement les clés primaires des objets associés.

6. **SlugRelatedField** : Ce champ permet de représenter les relations en utilisant 
un champ slug ou un champ unique d'un autre modèle.

7. **FileField** : Ce champ est utilisé pour gérer les téléchargements de fichiers dans votre API.

8. **ImageField** : Ce champ est spécifique pour gérer les images dans votre API.

Ces classes serializer sont très puissantes et flexibles, et elles peuvent être 
combinées et personnalisées pour répondre aux besoins spécifiques de votre application. 
Elles sont essentielles pour la création d'une API robuste et bien structurée avec Django REST Framework.
"""