FROM python:3.12-slim

RUN apt-get update && apt-get install -y redis-server

WORKDIR /app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY /src/ /app/
COPY docker-entrypoint.sh /app/


RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 6379

ENTRYPOINT ["/app/docker-entrypoint.sh"]
