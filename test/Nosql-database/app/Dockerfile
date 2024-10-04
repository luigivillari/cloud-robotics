FROM python:3.11-slim

WORKDIR /app

COPY conf.yaml /app/
COPY main.py /app/
COPY register.py /app/
COPY database.py /app/

RUN mkdir -p /app/logs

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Installare il pacchetto NTP
RUN apt-get update && apt-get install -y ntp

# Configurare il server NTP per sincronizzarsi con pool.ntp.org
RUN echo "server pool.ntp.org iburst" >> /etc/ntp.conf

# Copia lo script di avvio
COPY start.sh /app/

# Rendi lo script eseguibile
RUN chmod +x /app/start.sh

EXPOSE 1883

# Usa la sintassi JSON per eseguire lo script di avvio
CMD ["/app/start.sh"]
