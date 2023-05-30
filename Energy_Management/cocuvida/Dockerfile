FROM python:3
MAINTAINER Emil <emilbratt@mail.com>

RUN useradd -ms /bin/bash cocuvida
USER cocuvida
USER 1000:1000

ENV COCUVIDA_TESTING=false
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
WORKDIR /OTGT/Energy_Management/cocuvida/app

CMD ["python", "-m", "cocuvida"]
