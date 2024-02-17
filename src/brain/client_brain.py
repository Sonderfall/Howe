from sqs import request, wait_response, ThinkRequest


def think(utterance: str, on_new_sentence: callable) -> str:
    request(
        ThinkRequest(
            utterance=utterance,
            temperature=1,
            max_len=2048,
            top_k=20,
            top_p=1,
        )
    )

    whole_utterance = ""
    should_continue = True

    while should_continue:
        responses = wait_response()

        for response in responses:
            if response.end:
                should_continue = False
            else:
                on_new_sentence(response.utterance)
                whole_utterance += response.utterance + " "

    return whole_utterance


if __name__ == "__main__":
    print(think("Que pense tu des poneys unijambistes ?"))
