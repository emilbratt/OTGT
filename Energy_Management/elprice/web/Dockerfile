FROM python:3
MAINTAINER Emil <emilbratt@mail.com>
# URL - https://hub.docker.com/_/python

RUN useradd -ms /bin/bash elprice

USER elprice

USER 1000:1000

WORKDIR /app

CMD ["sh", "init.sh"]
#CMD ["python3", "main.py"]
