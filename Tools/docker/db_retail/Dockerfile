FROM mcr.microsoft.com/mssql/server:2022-latest
MAINTAINER Emil <emilbratt@mail.com>
# URL - https://hub.docker.com/_/microsoft-mssql-server


USER root

RUN mkdir /var/opt/sqlserver
RUN mkdir /var/opt/sqlserver/data
RUN mkdir /var/opt/sqlserver/log
RUN mkdir /var/opt/sqlserver/backup
RUN chown -R mssql /var/opt/sqlserver

RUN mkdir /var/opt/mssql/backup
RUN chown -R mssql /var/opt/mssql/backup


USER mssql

CMD /opt/mssql/bin/sqlservr
