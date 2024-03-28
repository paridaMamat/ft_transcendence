FROM python:3.10

#ne pas mettre en mémoire tampon la sortie standard et la sortie d'erreur. 
#Cela signifie que tout ce que votre code Python imprime sera immédiatement affiché sur la console, 
# sans aucun délai.
ENV PYTHONUNBUFFERED=1 

WORKDIR /app

COPY requirements.txt .

# Copiez le fichier manage.py dans le conteneur
COPY manage.py .

COPY /backend .

#COPY ./conf/postgresql.cnf /var/lib/postgresql/data/postgresql.cnf

EXPOSE 8000

RUN pip install python-decouple

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 
#&& daphne -e ssl:8000:privateKey=/cert/key.pem:certKey=/cert/cert.pem ft_transcendence.asgi:application