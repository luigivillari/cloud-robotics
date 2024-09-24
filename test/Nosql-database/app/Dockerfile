FROM python:3.11-slim


WORKDIR /app


COPY conf.yaml /app/


COPY main.py /app/
COPY register.py /app/
COPY database.py /app/

RUN mkdir -p /app/logs

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 1883 

CMD ["python", "main.py"]
