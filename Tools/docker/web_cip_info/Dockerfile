FROM php:8.0-apache
MAINTAINER Emil <emilbratt@mail.com>

RUN docker-php-ext-install pdo pdo_mysql

# adds directory for assets
RUN mkdir /cip_info_assets && chown 33:33 /cip_info_assets

RUN apt update && apt install freetds-bin tdsodbc -y

COPY ./freetds/freetds.conf /etc/freetds/freetds.conf
COPY ./freetds/odbcinst.ini /etc/odbcinst.ini
COPY ./freetds/odbc.ini /etc/odbc.ini
RUN odbcinst -i -d -f /usr/share/tdsodbc/odbcinst.ini

RUN apt update && apt install unixodbc unixodbc-dev -y \
 && docker-php-ext-configure pdo_odbc --with-pdo-odbc=unixODBC,/usr \
 && docker-php-ext-install pdo_odbc
