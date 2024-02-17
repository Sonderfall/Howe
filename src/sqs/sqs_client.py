import boto3
import os
import uuid

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Union, List


@dataclass_json
@dataclass
class SqsConfig:
    url: str
    access_key: str
    secret_key: str
    region: str


@dataclass_json
@dataclass
class ThinkRequest:
    utterance: str
    temperature: float
    max_len: int


@dataclass_json
@dataclass
class ThinkResponse:
    utterance: str
    end: bool


@dataclass
class _Queue:
    url: str
    name: str


def _config_from_file(config_filepath: str) -> SqsConfig:
    with open(config_filepath, "rb") as f:
        config = SqsConfig.from_json(f.read())

    return config


def _config_from_env() -> SqsConfig:
    return SqsConfig(
        url=os.environ["SQS_URL"],
        access_key=os.environ["SQS_ACCESS_KEY"],
        secret_key=os.environ["SQS_SECRET_KEY"],
        region=os.environ.get("SQS_REGION", "fr-par"),
    )


class SqsClient:
    def __init__(self, config_filepath: str) -> "SqsClient":
        self.__queues = {}

        if config_filepath is not None and os.path.exists(config_filepath):
            config = _config_from_file(config_filepath)
        else:
            config = _config_from_env()

        session = boto3.session.Session()

        self.__sqs_client = session.client(
            service_name="sqs",
            region_name=config.region,
            endpoint_url=config.url,
            aws_access_key_id=config.access_key,
            aws_secret_access_key=config.secret_key,
        )

    def create_queue(self, queue_name: str):
        real_queue_name = queue_name

        if not queue_name.endswith(".fifo"):
            real_queue_name = queue_name + ".fifo"

        try:
            queue = self.__sqs_client.create_queue(
                QueueName=real_queue_name,
                Attributes={
                    "MaximumMessageSize": str(4096),
                    "ReceiveMessageWaitTimeSeconds": "0",
                    "VisibilityTimeout": str(300),
                    "FifoQueue": "true",
                },
            )
        except:
            queue = self.__sqs_client.get_queue_url(QueueName=real_queue_name)
        finally:
            self.__queues[queue_name] = _Queue(url=queue["QueueUrl"], name=queue_name)

    def send_message(
        self, queue_name: str, message: Union[ThinkResponse, ThinkRequest]
    ) -> str:
        if not queue_name in self.__queues:
            return None

        queue = self.__queues[queue_name]

        msg = message.to_json()

        response = self.__sqs_client.send_message(
            QueueUrl=queue.url,
            MessageBody=msg,
            MessageAttributes={},
            MessageDeduplicationId=str(uuid.uuid4()),
        )

        return response.get("MessageId", None)

    def receive_messages(
        self, queue_name: str, max_msg: int, type: Union[ThinkResponse, ThinkRequest]
    ) -> List[Union[ThinkResponse, ThinkRequest]]:
        if not queue_name in self.__queues:
            return

        queue = self.__queues[queue_name]

        response = self.__sqs_client.receive_message(
            QueueUrl=queue.url,
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=max_msg,
            WaitTimeSeconds=10,
        )

        messages = response.get("Messages", [])
        array = []

        for msg in messages:
            body = msg["Body"]
            handler = msg["ReceiptHandle"]

            if type == ThinkResponse:
                array.append(ThinkResponse.from_json(body))
            elif type == ThinkRequest:
                array.append(ThinkRequest.from_json(body))

            self.__sqs_client.delete_message(QueueUrl=queue.url, ReceiptHandle=handler)

        return array

    def purge(self, queue_name: str):
        queue = self.__queues[queue_name]

        self.__sqs_client.purge_queue(
            QueueUrl=queue.url,
        )
