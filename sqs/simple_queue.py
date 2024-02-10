import boto3

class Sqs():
    def __init__(self, queue_name : str) -> "Sqs":
        sqs = boto3.resource("sqs")

        self.__queue = sqs.create_queue(QueueName=queue_name, Attributes={
            "MaximumMessageSize": str(4096),
            "ReceiveMessageWaitTimeSeconds": str(10),
            "VisibilityTimeout": str(300),
            "FifoQueue": str(True),
            })

    def send_message(self, message):
        response = self.__queue.send_message(
            MessageBody=message, MessageAttributes=None
        )

    def receive_messages(self) -> str:
        messages = self.__queue.receive_messages(
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10,
        )

        for msg in messages:
            return msg