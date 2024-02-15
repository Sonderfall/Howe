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

    @property
    def full_name(self):
        if self.namespace is not None:
            return f"{self.namespace}/{self.image}:{self.tag}"
        return f"{self.image}:{self.tag}"

    @property
    def name(self):
        if self.namespace is not None:
            return f"{self.namespace}/{self.image}"
        return self.image


@dataclass_json
@dataclass
class DockerHostConfig:
    host: str
    user: str
    port: str
    prefix: str


class DockerClient:
    def __init__(self, host_config: DockerHostConfig) -> "DockerClient":
        # Edit your ~/.ssh/config file like:
        # Host *
        #   User root
        #   IdentityFile ~/.ssh/id_rsa
        #   IdentitiesOnly no
        #   ForwardAgent no
        #   StrictHostKeyChecking no
        #   UserKnownHostsFile /dev/null
        self.__client = docker.client.APIClient(
            base_url=f"{host_config.prefix}{host_config.host}:{host_config.port}",
            tls=False,
            use_ssh_client=True,
        )

    def pull_image(self, img_config: DockerImageConfig) -> str:
        self.__client.pull(repository=img_config.name, tag=img_config.tag)

    def create_container(
        self, img_config: DockerImageConfig, ctn_config: DockerContainerConfig
    ) -> str:
        host_config = None

        if "gpu" in img_config.image:
            host_config = self.__client.create_host_config(
                device_requests=[
                    docker.types.DeviceRequest(
                        driver="nvidia", count="-1", capabilities=[["gpu"]]
                    )
                ]
            )

        self.__client.create_container(
            image=img_config.full_name,
            command=ctn_config.command,
            entrypoint=ctn_config.entrypoint,
            environment=ctn_config.env,
            hostname=ctn_config.name,
            name=ctn_config.name,
            host_config=host_config,
            detach=True,
        )
