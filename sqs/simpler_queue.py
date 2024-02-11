import time

from .simple_queue import Sqs, ThinkRequest, ThinkResponse


__REQUEST_QUEUE = "think_request_queue.fifo"
__RESPONSE_QUEUE = "think_response_queue.fifo"

__sqs_handler = Sqs("config/sqs.json")
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


def wait_response() -> ThinkResponse:
    while True:
        responses = __sqs_handler.receive_messages(__RESPONSE_QUEUE, 5, ThinkResponse)

        if len(responses) > 0:
            whole_utterance = ""

            for r in responses:
                whole_utterance += r.utterance + " "

            return ThinkResponse(
                utterance=whole_utterance,
                response_index=0,
                total_response_count=len(responses),
            )
        else:
            time.sleep(1)


if __name__ == "__main__":
    print(request(ThinkRequest(utterance="helloooo", temperature=0.5, max_len=512)))

    req = wait_request()
    print(req)

    print(
        respond(
            ThinkResponse(
                utterance="woooorld", total_response_count=1, response_index=0
            )
        )
    )

    resp = wait_response()
    print(resp)
