FROM python:3.11-slim


WORKDIR /app


COPY conf.yaml /app/
COPY main.py /app/
COPY task_manager.py /app/
COPY task_repository.py /app/

RUN mkdir -p /app/logs

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y ntp


RUN echo "server pool.ntp.org iburst" >> /etc/ntp.conf


COPY start.sh /app/

RUN chmod +x /app/start.sh

EXPOSE 1883 
CMD ["/app/start.sh"]
