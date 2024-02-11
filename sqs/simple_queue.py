import boto3

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Union, List


@dataclass_json
@dataclass
class SqsConfig:
    url: str
    access_key: str
    secret_key: str


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
    total_response_count: int
    response_index: int


@dataclass
class __Queue:
    url: str
    name: str


class Sqs:
    def __init__(self, config_filepath: str) -> "Sqs":
        self.__queues = {}

        with open(config_filepath, "rb") as f:
            config = SqsConfig.from_json(f.read())

            session = boto3.Session(
                aws_access_key_id=config.access_key,
                aws_secret_access_key=config.secret_key,
            )

            self.__sqs_client = session.resource("sqs")

    def create_queue(self, queue_name: str):
        if not queue_name.endswith(".fifo"):
            real_queue_name = queue_name + ".fifo"

        queue = self.__sqs_client.create_queue(
            QueueName=real_queue_name,
            Attributes={
                "MaximumMessageSize": str(4096),
                "ReceiveMessageWaitTimeSeconds": str(10),
                "VisibilityTimeout": str(300),
                "FifoQueue": str(True),
            },
        )

        self.__queues[queue_name] = __Queue(url=queue["QueueUrl"], name=queue_name)

    def send_message(
        self, queue_name: str, message: Union[ThinkResponse, ThinkRequest]
    ):
        if not queue_name in self.__queues:
            return

        queue = self.__queues[queue_name]

        response = self.__sqs_client.send_message(
            QueueUrl=queue.url, MessageBody=message.to_json(), MessageAttributes=None
        )

    def receive_messages(
        self, queue_name: str, max_msg: int, type: Union[ThinkResponse, ThinkRequest]
    ) -> List[Union[ThinkResponse, ThinkRequest]]:
        if not queue_name in self.__queues:
            return

        queue = self.__queues[queue_name]

        messages = self.__sqs_client.receive_messages(
            QueueUrl=queue.url,
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=max_msg,
            WaitTimeSeconds=10,
        )

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
