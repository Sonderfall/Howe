.PHONY: client
client:
	python3 src/main.py run --mode=client

.PHONY: server
server:
	python3 src/main.py run --mode=server

.PHONY: player
player:
	python3 src/player/browser.py --directory ./

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
	pip3 install --upgrade pip
	pip3 install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/
	pip install -r requirements-server.txt
	export PYTHONPATH=${PYTHONPATH}:$(pwd)/src

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

.PHONY: clear
clear:
	rm -rf tmp/