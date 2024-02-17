from sqs import request, wait_response, ThinkRequest
from threading import Thread

def think(utterance: str, on_new_sentence: callable) -> str:
    request(
        ThinkRequest(
            utterance=utterance,
            temperature=1,
            max_len=512,
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
                thread = Thread(target=on_new_sentence(response.utterance))
                thread.start()
                whole_utterance += response.utterance + " "

    return whole_utterance


if __name__ == "__main__":
    print(think("Que pense tu des poneys unijambistes ?"))
