FROM python:3.11-slim



#ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

EXPOSE 80

RUN apt-get update && \
    apt-get install -y curl wget gnupg ca-certificates fonts-liberation libasound2 libnss3 libcups2 libxss1 libxrandr2 libgconf-2-4
RUN pip install --upgrade pip setuptools wheel

COPY ./requirements.txt /var/requirements.txt
COPY ./src /App


RUN pip3 install -U pip && pip3 install --no-cache-dir -Ur /var/requirements.txt
RUN python -m playwright install chromium
RUN python -m playwright install chrome



WORKDIR /App