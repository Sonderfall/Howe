from sqs import ThinkRequest, ThinkResponse


def think(request: ThinkRequest) -> ThinkResponse:
    utterance = "Je vais bien, merci"

    response = ThinkResponse(utterance=utterance, end=True)

    return response


if __name__ == "__main__":
    print(
        think(
            ThinkRequest(
                utterance="Que penses tu des poneys unijambistes ?",
                temperature=1,
                max_len=512,
            )
        )
    )
