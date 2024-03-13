FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

EXPOSE 8080

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD python manage.py makemigrations && python manage.py migrate && daphne -e ssl:8080:privateKey=/cert/key.pem:certKey=/cert/cert.pem ft_transcendence.asgi:application
