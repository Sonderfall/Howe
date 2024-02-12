import docker

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DockerContainerConfig:
    name: str
    env: dict
    command: str
    entrypoint: str


@dataclass_json
@dataclass
class DockerImageConfig:
    image: str
    tag: str
    namespace: str
    password: str


@dataclass_json
@dataclass
class DockerHostConfig:
    host: str
    user: str


class DockerClient:
    def __init__(self, host_config: DockerHostConfig) -> "DockerClient":
        self.__client = docker.Client(base_url=host_config.host, tls=False)

    def pull_mage(self, img_config: DockerImageConfig) -> str:
        self.__client.images.pull(
            repository=f"{img_config.namespace}/{img_config.image}",
            tag=img_config.tag
            # auth_config={
            #     "username": img_config.namespace,
            #     "password": img_config.password,
            # },
        )

    def create_container(
        self, img_config: DockerImageConfig, ctn_config: DockerContainerConfig
    ) -> str:
        device_requests = None

        if img_config.image.contains("gpu"):
            device_requests = [
                docker.types.DeviceRequest(
                    driver="nvidia", count="-1", capabilities=[["gpu"]]
                )
            ]

        self.__client.containers.run(
            image=f"{img_config.namespace}/{img_config.image}",
            command=ctn_config.command,
            entrypoint=ctn_config.entrypoint,
            environment=ctn_config.env,
            hostname=ctn_config.name,
            device_requests=device_requests,
            detach=True,
        )
