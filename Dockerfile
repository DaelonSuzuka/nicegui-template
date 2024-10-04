# app/Dockerfile

FROM python:3.12

WORKDIR /app

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN uv venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# install dependencies
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
RUN uv sync

COPY ./src /app/src

EXPOSE 8080

CMD ["python", "src/main.py"]
