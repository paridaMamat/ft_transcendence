
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    champ1 = serializers.CharField(max_length=100)
    champ2 = serializers.EmailField()
    # Ajoutez d'autres champs selon vos besoins
