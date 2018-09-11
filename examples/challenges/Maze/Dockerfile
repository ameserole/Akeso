FROM node:4-onbuild
RUN apt update
RUN apt install python-pip -y
RUN pip install pika
RUN mkdir -p /usr/src/app
COPY server/ /usr/src/app/server
COPY public/ /usr/src/app/public
COPY node_modules /usr/src/app/node_modules/
COPY package.json /usr/src/app/package.json
RUN echo "flag" >> /flag.txt

EXPOSE 31337
