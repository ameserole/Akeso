FROM 32bit/ubuntu:16.04

RUN apt-get update
RUN apt-get install -y python-pip

COPY over_write_var /
COPY host_problem.py /
COPY flag.txt /

EXPOSE 4322
CMD ["python", "host_problem.py", "over_write_var", " 4322"]
