FROM python:3.9
MAINTAINER Emil <emilbratt@mail.com>

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
WORKDIR /code/app/Datawarehouse/server

# un-comment accordingly based on dev or prod env.
# for developement we want reload on file changes
CMD ["uvicorn", "barcode_generator.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
# for production we do not want reload on file change
#CMD ["uvicorn", "barcode_generator.main:app", "--host", "0.0.0.0", "--port", "80"]
# or if running behind a proxy like Traefik then we add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]


# NOTES:
#  building image..
#   $ docker build -t emil/barcode_generator:1.0 .
#  run:
#   $ docker run -d -it -p 8082:80 emil/barcode_generator:1.0
