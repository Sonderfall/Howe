.PHONY: client
client:
	python3 main.py --mode=client

.PHONY: server
server:
	python3 main.py --mode=server

.PHONY: install
install:
	pip3 install --upgrade pip
	pip install -r requirements.txt
