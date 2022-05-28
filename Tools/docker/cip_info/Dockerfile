FROM php:8.0-apache
MAINTAINER Emil <emilbratt@mail.com>

RUN docker-php-ext-install pdo pdo_mysql

# add directory for assets
# ..it will be used as a docker volume,
# ..but need to exist for us to set correct owner
RUN mkdir /cip_info_assets && chown 33:33 /cip_info_assets
