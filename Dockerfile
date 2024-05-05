FROM python:3.10-slim as requirements-stage

WORKDIR /tmp

RUN pip install --upgrade pip &&\
    pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-slim

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt requirements.txt

RUN apt-get update \
  && apt-get -y install netcat-traditional \
  && apt-get clean

RUN pip install --upgrade pip &&\
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY /scripts/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY alembic.ini /app/alembic.ini
COPY /src /app/src

ENV PYTHONPATH /app/src:$PYTHONPATH
ENTRYPOINT ["/app/entrypoint.sh"]
