FROM python:3
MAINTAINER Emil <emilbratt@mail.com>

RUN useradd -ms /bin/bash elprice
USER elprice
USER 1000:1000

# will not be able to start uvicorn unless we add this to PATH
ENV PATH /home/elprice/.local/bin:${PATH}
COPY ./requirements.txt /requirements.txt
RUN pip install --user --no-cache-dir --upgrade -r /requirements.txt
WORKDIR /OTGT/Energy_Management/elprice/web_datastore/app


# un-comment accordingly based on dev or prod env.
# for developement we want reload on file changes
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8085"]
# for production we do not want reload on file change
#CMD ["uvicorn", "spreadsheet_generator.main:app", "--host", "0.0.0.0", "--port", "8082"]
# or if running behind a proxy like Traefik then we add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8082", "--proxy-headers"]
