FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /srv/proxy

COPY docker/proxy/proxy_placeholder.py /srv/proxy/proxy_placeholder.py

EXPOSE 8080

CMD ["python", "/srv/proxy/proxy_placeholder.py"]
