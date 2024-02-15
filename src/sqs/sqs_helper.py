import time

from typing import List
from sqs.sqs_client import SqsClient, ThinkRequest, ThinkResponse


__REQUEST_QUEUE = "think_request_queue.fifo"
__RESPONSE_QUEUE = "think_response_queue.fifo"

__sqs_handler = SqsClient("config/sqs.json")
__sqs_handler.create_queue(__REQUEST_QUEUE)
__sqs_handler.create_queue(__RESPONSE_QUEUE)


def request(req: ThinkRequest) -> str:
    return __sqs_handler.send_message(__REQUEST_QUEUE, req)


def respond(resp: ThinkResponse) -> str:
    return __sqs_handler.send_message(__RESPONSE_QUEUE, resp)


def wait_request() -> ThinkRequest:
    while True:
        responses = __sqs_handler.receive_messages(__REQUEST_QUEUE, 1, ThinkRequest)

        if len(responses) > 0:
            return responses[0]
        else:
            time.sleep(1)


def wait_response() -> List[ThinkResponse]:
    while True:
        responses = __sqs_handler.receive_messages(__RESPONSE_QUEUE, 10, ThinkResponse)

        if len(responses) > 0:
            return responses
            # whole_utterance = ""

        # for r in responses:
        #     # whole_utterance += r.utterance + " "

        #     return ThinkResponse(
        #         utterance=whole_utterance,
        #         end=True,
        #     )
        else:
            time.sleep(1)


if __name__ == "__main__":
    print(request(ThinkRequest(utterance="helloooo", temperature=0.5, max_len=512)))

    print(wait_request())

    print(
        respond(
            ThinkResponse(
                utterance="woooorld",
                end=True,
            )
        )
    )

    print(wait_response())
