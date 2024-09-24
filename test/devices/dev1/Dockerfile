FROM python:3.11-slim


WORKDIR /app


COPY requirements.txt /app/


RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir -r requirements.txt


RUN curl -SL https://github.com/docker/compose/releases/download/v2.29.6/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose


COPY . /app/

EXPOSE 1883

CMD ["python3","agente.py"]
