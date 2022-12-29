FROM python:3
MAINTAINER Emil <emilbratt@mail.com>
# URL - https://hub.docker.com/_/python

RUN useradd -ms /bin/bash elprice

USER elprice

USER 1000:1000

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

WORKDIR /app

CMD ["sh", "init.sh"]
#CMD ["python3", "main.py"]
