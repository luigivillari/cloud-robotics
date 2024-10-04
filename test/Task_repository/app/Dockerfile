FROM python:3.11-slim


WORKDIR /app


COPY conf.yaml /app/
COPY main.py /app/
COPY task_manager.py /app/
COPY task_repository.py /app/

RUN mkdir -p /app/logs

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Installare il pacchetto NTP
RUN apt-get update && apt-get install -y ntp

# Configurare il server NTP per sincronizzarsi con pool.ntp.org
RUN echo "server pool.ntp.org iburst" >> /etc/ntp.conf

# Assicurarsi che ntpd parta all'avvio del container
COPY start.sh /app/

RUN chmod +x /app/start.sh

EXPOSE 1883 
CMD ["/app/start.sh"]
