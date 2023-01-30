FROM postgres:15.1

ENV POSTGRES_USER $username
ENV POSTGRES_PASSWORD $password
ENV POSTGRES_DB $db

RUN apt-get update && \
    apt-get install -y git python3-pip python3-dev libpq-dev

WORKDIR /opt/
RUN git clone https://github.com/epicosy/tenet-db.git

WORKDIR /opt/tenet-db
RUN pip install .
COPY init-db.sh /docker-entrypoint-initdb.d/
WORKDIR ~
