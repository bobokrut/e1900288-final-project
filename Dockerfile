FROM python:3.10.4-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.poetry/bin:/venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libtiff5-dev libjpeg62-turbo-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev libpq-dev && rm -rf /var/lib/apt/lists/*

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential curl && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN python -m venv /venv

COPY pyproject.toml poetry.lock .
RUN . /venv/bin/activate && poetry update && poetry install --no-dev --no-root


FROM base as final

COPY . .

COPY --from=builder /venv /venv

ENTRYPOINT ["/venv/bin/gunicorn"]
CMD ["-b", "0.0.0.0:8000", "app:create_app()"]
