from sqs import request, wait_response, ThinkRequest


def think(utterance: str) -> str:
    request(
        ThinkRequest(
            utterance=utterance,
            temperature=0.5,
            max_len=512,
        )
    )

    response = wait_response()

    return response.utterance


if __name__ == "__main__":
    pass
