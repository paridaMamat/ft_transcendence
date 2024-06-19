#!/bin/sh
# python manage.py migrate website zero --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create superuser if not exists
# If superuser exists, update password

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
	if [ "$(python manage.py shell -c "from website.models.CustomUser import CustomUser; print(CustomUser.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())")" = "True" ]
	then
		python manage.py shell -c "from website.models.CustomUser import CustomUser; u = CustomUser.objects.get(username='$DJANGO_SUPERUSER_USERNAME'); u.set_password('$DJANGO_SUPERUSER_PASSWORD'); u.save()"
	else
    	python manage.py createsuperuser \
			--noinput \
			--username $DJANGO_SUPERUSER_USERNAME \
			--email $DJANGO_SUPERUSER_EMAIL
	fi
fi

#python manage.py add_default_data
# python load_custom_data.py

python manage.py loaddata user_data.json

python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000