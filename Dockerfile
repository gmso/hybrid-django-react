# Pull base image
FROM python:3.7

# GNU's gettext used for Django's internationalization
RUN apt-get update \
 && apt-get install -y gettext

# Environment variables available for containers
ENV ENVIRONMENT=${DJANGO_ENVIRONMENT} \
  SECRET_KEY=${DJANGO_SECRET_KEY} \
  DEBUG=${DJANGO_DEBUG} \
  PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.8

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization with its dependencies, without virtual environment (not needed in Docker containers)
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$ENVIRONMENT" == production && echo "--no-dev") --no-interaction --no-ansi

# Copy project
COPY . /code/
