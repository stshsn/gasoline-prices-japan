FROM python:3.12.8-slim-bullseye AS builder

WORKDIR /opt/app
RUN pip3 install poetry
COPY pyproject.toml poetry.toml poetry.lock ./
RUN poetry install --only main


FROM python:3.12.8-slim-bullseye AS runner

RUN useradd -r -s /bin/false uvicornuser
WORKDIR /opt/app
COPY --from=builder /opt/app/.venv /opt/app/.venv
COPY gasoline_prices ./gasoline_prices
USER uvicornuser

EXPOSE 8000
CMD ["/opt/app/.venv/bin/gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--capture-output", "--log-level", "warning", "--access-logfile", "-", "--bind", ":8000", "gasoline_prices.main:app"]
