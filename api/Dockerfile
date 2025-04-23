FROM python:3.12

#ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

EXPOSE 80

COPY ./requirements.txt /var/requirements.txt
COPY ./src /App

RUN pip install -U pip && pip install --no-cache-dir -Ur /var/requirements.txt
RUN playwright install chromium

WORKDIR /App