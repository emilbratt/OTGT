FROM python:3
MAINTAINER Emil <emilbratt@mail.com>
# URL - https://hub.docker.com/_/python

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
WORKDIR /code/app/Datawarehouse/server

# un-comment accordingly based on dev or prod env.
# for developement we want reload on file changes
CMD ["uvicorn", "spreadsheet_generator.main:app", "--reload", "--host", "0.0.0.0", "--port", "8082"]
# for production we do not want reload on file change
#CMD ["uvicorn", "spreadsheet_generator.main:app", "--host", "0.0.0.0", "--port", "8082"]
# or if running behind a proxy like Traefik then we add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8082", "--proxy-headers"]
