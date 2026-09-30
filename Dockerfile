FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:$PATH"
WORKDIR /app

RUN addgroup --system enigma && adduser --system --ingroup enigma --home /app enigma
COPY pyproject.toml uv.lock README.md ./
COPY enigma ./enigma
COPY migrations ./migrations
COPY alembic.ini docker-entrypoint.sh ./
RUN pip install --no-cache-dir uv==0.12.19 \
    && uv sync --frozen --no-dev --no-editable \
    && rm -rf /root/.cache/uv /root/.cache/pip \
    && chmod 0555 /app/docker-entrypoint.sh
USER enigma
EXPOSE 8000
HEALTHCHECK --interval=20s --timeout=4s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/ready', timeout=3)" || exit 1
ENTRYPOINT ["/app/docker-entrypoint.sh"]
