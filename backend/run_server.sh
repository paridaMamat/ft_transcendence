#!/bin/sh

# Spécifiez explicitement l'interpréteur Python
#PYTHON="/usr/local/bin/python"

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Créez un superutilisateur s'il n'existe pas
# Si le superutilisateur existe, mettez à jour le mot de passe
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    if [ "$(python manage.py shell -c "from website.models import CustomUser; print(CustomUser.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())")" = "True" ]
    then
        python manage.py shell -c "from website.models import CustomUser; u = CustomUser.objects.get(username='$DJANGO_SUPERUSER_USERNAME'); u.set_password('$DJANGO_SUPERUSER_PASSWORD'); u.save()"
    else
        python manage.py createsuperuser \
            --noinput \
            --username $DJANGO_SUPERUSER_USERNAME \
            --email $DJANGO_SUPERUSER_EMAIL
    fi
fi

# Décommentez les lignes suivantes si vous devez exécuter des commandes supplémentaires
python manage.py add_default_data
python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000

