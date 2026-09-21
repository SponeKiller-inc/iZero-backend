FROM python:3.11-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Build toolchain for psycopg2 – only needed in the builder stage
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build
COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# libpq5 for psycopg2, postgresql-client for pg_isready in the entrypoint
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq5 \
       postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

WORKDIR /srv

COPY . .

RUN chmod +x /srv/entrypoint.sh \
    && useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /srv

USER appuser

EXPOSE 8000
ENTRYPOINT ["/srv/entrypoint.sh"]
CMD ["uvicorn", "app.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]