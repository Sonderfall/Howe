from sqs import ThinkRequest, ThinkResponse


def think(request: ThinkRequest) -> ThinkResponse:
    utterance = "Je vais bien, merci"

    response = ThinkResponse(
        utterance=utterance, total_response_count=1, response_index=0
    )

    return response


if __name__ == "__main__":
    print(
        think(
            ThinkRequest(
                utterance="Que penses tu des poneys unijambistes ?",
                temperature=0.6,
                max_len=512,
            )
        )
    )
