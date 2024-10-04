FROM python:3.11-slim


WORKDIR /app


COPY requirements.txt /app/

RUN mkdir -p /app/logs

RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir -r requirements.txt
# Installare il pacchetto NTP
RUN apt-get update && apt-get install -y ntp

# Configurare il server NTP per sincronizzarsi con pool.ntp.org
RUN echo "server pool.ntp.org iburst" >> /etc/ntp.conf

# Assicurarsi che ntpd parta all'avvio del container

RUN curl -SL https://github.com/docker/compose/releases/download/v2.29.6/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose


COPY . /app/

RUN chmod +x /app/start.sh

EXPOSE 1883

CMD ["/app/start.sh"]
