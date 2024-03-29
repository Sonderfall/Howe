import os
import time

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from scaleway import Client
from scaleway.marketplace.v1 import MarketplaceV1API
from scaleway.instance.v1 import InstanceV1API
from scaleway.instance.v1.types import (
    Server,
    ServerState,
    ServerAction,
    IpType,
)


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

    def __get_image_id(self, image_name: str) -> str:
        marketplace_api = MarketplaceV1API(self.__scw_client)
        images = marketplace_api.list_images_all(page=0, per_page=100)

        for image in images:
            if image is not None and image.label == image_name:
                latest_version = image.versions[0]

                for local_img in latest_version.local_images:
                    if local_img.zone == self.__scw_client.default_zone:
                        return local_img.id

        return None

    def create_instance(self, name: str, config: ScalewayInstanceConfig) -> Server:
        instance_api = InstanceV1API(self.__scw_client)

        print("Getting docker image...")
        img_id = self.__get_image_id(config.image)

        if img_id is None:
            print("Got None image.")
            return None

        print("Creating ip...")
        ip_res = instance_api.create_ip(type_=IpType.UNKNOWN_IPTYPE)

        print("Creating server...")
        serv_res = instance_api._create_server(
            commercial_type=config.type,
            image=img_id,
            name=name,
            public_ip=ip_res.ip.id,
            enable_ipv6=True,
        )

        if serv_res is None or serv_res.server is None:
            print("Got None server.")
            return None

        print("Starting server...")
        instance_api.server_action(
            server_id=serv_res.server.id, action=ServerAction.POWERON
        )

        while serv_res.server.state != ServerState.RUNNING:
            serv_res = instance_api.get_server(
                server_id=serv_res.server.id,
            )
            time.sleep(3)

        print("Server fully started.")

        return serv_res.server

    def destroy_instance(self, id: str):
        instance_api = InstanceV1API(self.__scw_client)

        serv_res = instance_api.get_server(
            server_id=id,
        )

        if serv_res is None or serv_res.server is None:
            print("Got null server.")
            return

        if serv_res.server.state != ServerState.RUNNING:
            print("Server not running")
            return

        print("Stopping server...")
        instance_api.server_action(
            server_id=serv_res.server.id, action=ServerAction.POWEROFF
        )

        while serv_res.server.state != ServerState.STOPPED:
            serv_res = instance_api.get_server(
                server_id=id,
            )
            time.sleep(3)

        print("Destroying server...")
        instance_api.delete_server(
            server_id=serv_res.server.id,
        )

        print("Destroying ip...")
        instance_api.delete_ip(
            ip=serv_res.server.public_ip.id,
        )

        print("Destroying volumes...")
        for _, volume in serv_res.server.volumes.items():
            instance_api.delete_volume(volume_id=volume.id)

        print("Server fully destroyed.")
