FROM python:3.11

WORKDIR usr/

COPY requirements.txt .
RUN pip install -r requirements.txt
