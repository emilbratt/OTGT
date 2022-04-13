FROM mariadb
MAINTAINER Emil <emilbratt@mail.com>
# URL - https://hub.docker.com/_/mariadb

RUN apt-get update && apt-get upgrade -y

# container will call these scripts on first boot in alphabetical order
COPY ./tables.sql /docker-entrypoint-initdb.d/1_tables.sql
COPY ./permissions.sql /docker-entrypoint-initdb.d/2_permissions.sql
