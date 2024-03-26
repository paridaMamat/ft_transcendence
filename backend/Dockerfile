FROM python:3.10

#ne pas mettre en mémoire tampon la sortie standard et la sortie d'erreur. 
#Cela signifie que tout ce que votre code Python imprime sera immédiatement affiché sur la console, 
# sans aucun délai.
ENV PYTHONUNBUFFERED=1 

WORKDIR /app

COPY requirements.txt .
# Copiez le fichier manage.py dans le conteneur
COPY manage.py .

EXPOSE 8080

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD python manage.py runserver

#CMD python manage.py makemigrations && python manage.py migrate 
#&& daphne -e ssl:8080:privateKey=/cert/key.pem:certKey=/cert/cert.pem ft_transcendence.asgi:application