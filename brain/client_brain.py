from sqs import request, wait_response, ThinkRequest


def think(utterance: str) -> str:
    # Send Sqs message with utterance
    request(ThinkRequest(
        utterance=utterance,
        temperature=0.5,
        max_len=512,
    ))

    # Aggregate multiple responses
    response = wait_response()

    return response.utterance


if __name__ == "__main__":
    pass
