FROM ubuntu:latest

RUN apt update
RUN apt-get update
RUN apt install python openssh-server -y
RUN groupadd ctf-users
ADD . ./
RUN apt update
RUN ./ctfd/prepare.sh

RUN pip install pika

RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config
RUN sed -i 's/StrictModes yes/#StrictModes yes/g' /etc/ssh/sshd_config
RUN service ssh restart

EXPOSE 4001
EXPOSE 22
