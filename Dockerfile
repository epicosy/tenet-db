FROM python:3.10

#RUN apt-get update && \ 
#    apt-get install -y git python3-pip python3-dev libpq-dev

WORKDIR /opt
RUN git clone https://github.com/epicosy/tenet-db.git

WORKDIR /opt/tenet-db
RUN pip install .

WORKDIR ~
