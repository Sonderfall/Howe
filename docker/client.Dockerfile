FROM python:3.11

COPY src .
COPY requirements-client.txt .
COPY Makefile .

RUN make install-client

ENTRYPOINT [ "make", "client" ]