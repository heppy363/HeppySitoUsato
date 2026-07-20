FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.1.4
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /workspace/backend

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY backend/pyproject.toml backend/poetry.lock backend/README.md ./
RUN poetry install --only main --no-root

COPY backend/app ./app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
