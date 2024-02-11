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

.PHONY: install-llama-cpp
install-llama-cpp:
	sudo apt install nvidia-cuda-toolkit
	pip3 install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/
# set CMAKE_ARGS=-DLLAMA_CUBLAS=on
# set FORCE_CMAKE=1
# pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
