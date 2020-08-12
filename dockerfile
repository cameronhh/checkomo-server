FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./ /app

RUN pip install -r requirements.txt

ENV NGINX_WORKER_PROCESSES 2
ENV NGINX_WORKER_CONNECTIONS 1024
ENV LISTEN_PORT 80
EXPOSE 80