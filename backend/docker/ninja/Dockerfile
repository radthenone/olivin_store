# base stage
FROM python:3.11.7 AS base

# build stage
FROM base AS build

WORKDIR /build

RUN apt update && \
    apt install -y --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && apt purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip wheel --wheel-dir /usr/src/app/wheels  \
    -r requirements.txt

# runtime stage
FROM base AS runtime

ENV BUILD_ENV=dev \
    # python:
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDEVMODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

COPY --from=build /usr/src/app/wheels  /wheels/

RUN python -m pip install --no-cache-dir uv

RUN uv pip install --system --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./docker/celery/beat.sh /celery/beat.sh
RUN sed -i 's/\r$//g' /celery/beat.sh && chmod +x /celery/beat.sh

COPY ./docker/celery/worker.sh /celery/worker.sh
RUN sed -i 's/\r$//g' /celery/worker.sh && chmod +x /celery/worker.sh

COPY ./docker/celery/flower.sh /celery/flower.sh
RUN sed -i 's/\r$//g' /celery/flower.sh && chmod +x /celery/flower.sh

COPY ./docker/django.sh /django.sh
RUN sed -i 's/\r$//g' /django.sh && chmod +x /django.sh

COPY ./docker/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

COPY . /app

ENTRYPOINT ["/entrypoint.sh"]
