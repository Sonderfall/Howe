import os

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from scaleway_client import ScalewayClient, ScalewayInstanceConfig
from docker_client import (
    DockerClient,
    DockerHostConfig,
    DockerContainerConfig,
    DockerImageConfig,
)

__SAVE_FILE = "config/instance.json"

__instance_config = ScalewayInstanceConfig(
    type="RENDER-S",
    image="ubuntu_jammy_gpu_os_12",
    user="root",
)

__image_config = DockerImageConfig(
    namespace="sonderfall",
    image="howe",
    tag="latest",
)


@dataclass_json
@dataclass
class __SavedState:
    server_id: str
    container_id: str


def __save(state: __SavedState):
    with open(__SAVE_FILE, "wb") as out:
        out.write(state.to_json())


def __load() -> __SavedState:
    if not os.path.exists(__SAVE_FILE):
        return __SavedState()

    with open(__SAVE_FILE, "rb") as f:
        state = __SavedState.from_json(f.read())

    return state


def spawn():
    scw_client = ScalewayClient("config/scaleway.json")
    srv = scw_client.create_instance("my-instance", __instance_config)

    __save(__SavedState(server_id=srv.id))

    docker_client = DockerClient(
        DockerHostConfig(
            host=srv.public_ip.address,
            user=__instance_config.user,
        )
    )

    docker_client.pull_image(__image_config)

    docker_client.create_container(
        __image_config,
        DockerContainerConfig(
            name="",
            env={},
            command="",
            entrypoint="",
        ),
    )

    __save(__SavedState(server_id=srv.id, container_id=""))


def kill():
    scw_client = ScalewayClient("config/scaleway.json")
    state = __load()
    scw_client.destroy_instance(state.server_id)