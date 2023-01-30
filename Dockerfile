FROM postgresql:15.1

ENV POSTGRES_USER $username
ENV POSTGRES_PASSWORD $password
ENV POSTGRES_DB $db

RUN git clone https://github.com/epicosy/tenet-db.git
WORKDIR tenet-db
RUN pip install .
WORKDIR ~

CMD tenetdb --dialect postgresql --username $username --password $password --host localhost --database $db --port 5432
