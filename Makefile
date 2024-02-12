.PHONY: client
client:
	python3 src/main.py run --mode=client

.PHONY: server
server:
	python3 src/main.py run --mode=server

.PHONY: build-server
build-server:
	docker build -f docker/server.Dockerfile --tag sonderfall/howe:latest .
	docker login --username ${DOCKER_USER} --password ${DOCKER_PWD}
	docker push sonderfall/howe:latest

.PHONY: install-client
install-client:
	pip3 install --upgrade pip
	pip install -r requirements-client.txt

.PHONY: install-server
install-server:
# sudo apt install nvidia-cuda-toolkit
	pip3 install --upgrade pip
	pip3 install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/
	pip install -r requirements-server.txt

.PHONY: install-controller
install-controller:
	pip3 install --upgrade pip
	pip install -r requirements-controller.txt

.PHONY: spawn-server
spawn-server:
	python3 src/main.py spawn

.PHONY: kill-server
kill-server:
	python3 src/main.py kill