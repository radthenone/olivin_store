#build stage
FROM python:3.11 AS base

ARG BUILD_ENVIRONMENT=dev
ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.8 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt update && \
    apt install -y --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

FROM base AS build

WORKDIR /app

COPY pyproject.toml ./

RUN python -m pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    poetry lock --no-update && \
    poetry install $(if [ "$BUILD_ENVIRONMENT" = "dev" ]; then echo "--with dev"; fi) --no-interaction --no-ansi --no-root --no-cache \
    && rm -rf "$POETRY_CACHE_DIR"

# dev stage
FROM build AS dev

COPY --from=build /app /src

WORKDIR /src

COPY ./docker/django.sh /django.sh
RUN sed -i 's/\r$//g' /django.sh && chmod +x /django.sh

COPY ./docker/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

COPY . /src

ENTRYPOINT ["/entrypoint.sh"]