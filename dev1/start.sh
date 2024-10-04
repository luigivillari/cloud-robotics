#!/bin/bash

# Avvia il servizio NTP
ntpd -g

# Esegui il programma Python
python /app/agente.py
