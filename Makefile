.PHONY: client
client:
	python3 main.py --mode=client

.PHONY: server
server:
	python3 main.py --mode=server

.PHONY: install-client
install-client:
	pip3 install --upgrade pip
	pip install -r requirements-client.txt

.PHONY: install-server
install-server:
	sudo apt install nvidia-cuda-toolkit
	pip3 install --upgrade pip
	pip3 install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/
	pip install -r requirements-server.txt
