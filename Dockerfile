FROM python:3.8.7-slim-buster

#RUN apt update && apt install -y gettext

RUN pip install -U pip wheel poetry

RUN python -m venv /venv

ADD pyproject.toml poetry.lock /app/

RUN cd app \
 && . /venv/bin/activate \
 && poetry install

ADD . /app
WORKDIR /app

EXPOSE 8080
CMD ["./docker-entrypoint.sh"]
