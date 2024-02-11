FROM python:3.11

COPY src .
COPY requirements-server.txt .
COPY Makefile .

RUN make install-server

ENTRYPOINT [ "make", "server" ]