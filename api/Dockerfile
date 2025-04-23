FROM python:3.12

FROM ubuntu:latest


#ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

EXPOSE 80

COPY ./requirements.txt /var/requirements.txt
COPY ./src /App

# Обновляем систему и устанавливаем необходимые пакеты
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common wget curl git ca-certificates gnupg locales-all unzip build-essential libssl-dev libffi-dev python3-pip python3-dev

# Устанавливаем Node.js и npm
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

RUN pip3 install -U pip && pip3 install --no-cache-dir -Ur /var/requirements.txt

# Установка Playwright
RUN npm install -g @playwright/test
RUN npx playwright install-deps chromium


WORKDIR /App