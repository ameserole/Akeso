FROM python:2.7-alpine
RUN apk update && \
    apk add python python-dev libffi-dev gcc make musl-dev py-pip mysql-client

RUN mkdir -p /opt/CTFd
COPY . /opt/CTFd
WORKDIR /opt/CTFd
VOLUME ["/opt/CTFd"]

RUN pip install -r requirements.txt

RUN chmod +x /opt/CTFd/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/opt/CTFd/docker-entrypoint.sh"]
