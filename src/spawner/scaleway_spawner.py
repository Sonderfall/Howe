import os

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from spawner.scaleway_client import ScalewayClient, ScalewayInstanceConfig
from spawner.docker_client import (
    DockerClient,
    DockerHostConfig,
    DockerContainerConfig,
    DockerImageConfig,
)

__SAVE_FILE = "config/instance.json"

# __instance_config = ScalewayInstanceConfig(
#     type="RENDER-S",
#     image="ubuntu_jammy_gpu_os_12",
#     user="root",
# )

__instance_config = ScalewayInstanceConfig(
    type="DEV1-S",
    image="docker",
    user="root",
)

# __image_config = DockerImageConfig(
#     namespace="sonderfall",
#     image="howe",
#     tag="latest",
# )


__image_config = DockerImageConfig(
    namespace=None,
    image="postgres",
    tag="latest",
)


@dataclass_json
@dataclass
class __SavedState:
    server_id: str


def __save(state: __SavedState):
    with open(__SAVE_FILE, "w") as out:
        out.write(state.to_json())


def __load() -> __SavedState:
    if not os.path.exists(__SAVE_FILE):
        return __SavedState()

    with open(__SAVE_FILE, "r") as f:
        state = __SavedState.from_json(f.read())

    return state


def spawn():
    scw_client = ScalewayClient("config/scaleway.json")
    srv = scw_client.create_instance("my-instance", __instance_config)

    __save(__SavedState(server_id=srv.id))

    docker_client = DockerClient(
        DockerHostConfig(
            prefix="ssh://",
            port="22",
            host=srv.public_ip.address,
            # host="51.159.128.172",
            user=__instance_config.user,
        )
    )

    docker_client.pull_image(__image_config)

    docker_client.create_container(
        __image_config,
        DockerContainerConfig(
            command=None,
            entrypoint=None,
            name="my-server",
            env={
                "SQS_URL": "",
                "SQS_ACCESS_KEY": "",
                "SQS_SECRET_KEY": "",
                "SQS_REGION": "",
            },
        ),
    )


def kill():
    scw_client = ScalewayClient("config/scaleway.json")
    state = __load()
    scw_client.destroy_instance(state.server_id)
