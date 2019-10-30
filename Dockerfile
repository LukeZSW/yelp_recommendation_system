FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV LISTEN_PORT 8080

EXPOSE 8080

ENV NGINX_WORKER_PROCESSES auto

ENV STATIC_PATH /app/app/static

COPY ./app /app/app

COPY uwsgi.ini /app/uwsgi.ini

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /app