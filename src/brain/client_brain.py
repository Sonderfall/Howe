from sqs import request, wait_response, ThinkRequest


def think(utterance: str, on_new_sentence: callable) -> str:
    request(
        ThinkRequest(
            utterance=utterance,
            temperature=1,
            max_len=512,
        )
    )

    whole_utterance = ""
    current_sentence = ""
    should_continue = True

    while should_continue:
        responses = wait_response()

        for response in responses:
            current_sentence += response.utterance + " "
            if response.end:
                should_continue = False

        if (
            "." in response.utterance
            or "?" in response.utterance
            or "!" in response.utterance
            or ";" in response.utterance
            or ":" in response.utterance
            # or "," in response.utterance
        ):
            whole_utterance += current_sentence
            on_new_sentence(current_sentence)
            current_sentence = ""

    return whole_utterance


if __name__ == "__main__":
    print(think("Que pense tu des poneys unijambistes ?"))
