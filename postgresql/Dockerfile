FROM postgres:latest

ENV POSTGRES_PASSWORD postgres

#RUN echo "locale: en_US.UTF-8" >> /etc/postgresql/14/main/postgresql.conf

EXPOSE 5432

COPY dbscript.sh ./

RUN chmod +x ./dbscript.sh

ENTRYPOINT ["bash", "./dbscript.sh"]
