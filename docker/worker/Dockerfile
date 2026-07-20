FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /srv/worker

COPY docker/worker/worker.py /srv/worker/worker.py

CMD ["python", "/srv/worker/worker.py"]
