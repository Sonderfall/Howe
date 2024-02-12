import os

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from scaleway import Client
from scaleway.instance.v1 import InstanceV1API
from scaleway.instance.v1.types import Server, ServerAction, IpType


@dataclass_json
@dataclass
class ScalewayInstanceConfig:
    type: str
    image: str
    user: str


@dataclass_json
@dataclass
class _ScalewayConfig:
    access_key: str
    secret_key: str
    project_id: str
    region: str
    az: str


def _config_from_file(config_filepath: str) -> _ScalewayConfig:
    with open(config_filepath, "rb") as f:
        config = _ScalewayConfig.from_json(f.read())

    return config


def _config_from_env() -> _ScalewayConfig:
    return _ScalewayConfig(
        secret_key=os.environ["SCW_SECRET_KEY"],
        access_key=os.environ["SCW_ACCESS_KEY"],
        project_id=os.environ["SCW_PROJECT_ID"],
        region=os.environ.get("SCW_REGION", "fr-par"),
        az=os.environ.get("SCW_AZ", "fr-par-2"),
    )


class ScalewayClient:
    def __init__(self, config_filepath: str) -> "ScalewayClient":
        if config_filepath is not None and os.path.exists(config_filepath):
            config = _config_from_file(config_filepath)
        else:
            config = _config_from_env()

        self.__scw_client = Client(
            access_key=config.access_key,
            secret_key=config.secret_key,
            default_project_id=config.project_id,
            default_region=config.region,
            default_zone=config.az,
        )

    def create_instance(self, name: str, config: ScalewayInstanceConfig) -> Server:
        instance_api = InstanceV1API(self.__scw_client)

        print("Creating ip...")

        ip_res = instance_api.create_ip(type_=IpType.UNKNOWN_IPTYPE)

        print("Creating server...")

        serv_res = instance_api._create_server(
            commercial_type=config.type,
            image=config.image,
            name=name,
            public_ip=ip_res.ip.id,
            enable_ipv6=True,
        )

        print("Starting server...")

        instance_api.server_action(
            server_id=serv_res.server.id, action=ServerAction.POWERON
        )

        return serv_res.Server

    def destroy_instance(self, id: str):
        instance_api = InstanceV1API(self.__scw_client)

        serv_res = instance_api.get_server(
            server_id=id,
        )

        if serv_res is None:
            return

        print("Stopping server...")

        instance_api.server_action(
            server_id=serv_res.server.id, action=ServerAction.POWEROFF
        )

        print("Destroying server...")

        instance_api.delete_server(
            server_id=serv_res.server.id,
        )

        print("Destroying ip...")

        instance_api.delete_ip(
            ip=serv_res.server.public_ip.id,
        )

        print("Destroying volumes...")

        for volume in serv_res.server.volumes:
            instance_api.delete_volume(volume_id=volume.id)
