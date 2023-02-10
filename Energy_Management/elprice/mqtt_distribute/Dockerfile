FROM python:3
MAINTAINER Emil <emilbratt@mail.com>

RUN useradd -ms /bin/bash elprice
USER elprice
USER 1000:1000
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
WORKDIR /OTGT/Energy_Management/elprice/mqtt_distribute/app

# init production
#CMD ["python3", "main.py"]
# init dev
# unbuffered output (-u) to use if nothing is shown in tty (will not wait until x lines are printed)
CMD ["python3", "-u", "main.py"]
