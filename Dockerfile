FROM python:3.9.6-slim as builder

ENV POETRY_VIRTUALENVS_CREATE false
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

COPY poetry.lock pyproject.toml ./

RUN pip install poetry --no-cache-dir
RUN poetry install --no-root --no-interaction --no-ansi

FROM builder

WORKDIR /app
COPY . .

RUN cp -n .env.sample .env

EXPOSE 8000

ENTRYPOINT ./docker-entrypoint.sh
