from llama import Llama
from sqs import ThinkRequest, ThinkResponse


__generator = Llama.build(
    ckpt_dir="../llama/llama-2-7b-chat",
    tokenizer_path="../llama/tokenizer.model",
    max_seq_len=1024,
    max_batch_size=1,
)


def think(request: ThinkRequest) -> ThinkResponse:
    dialogs = [
        [{"role": "user", "content": request.utterance}],
    ]

    results = __generator.chat_completion(
        dialogs,
        max_gen_len=request.max_len,
        temperature=request.temperature,
        top_p=0.9,
    )

    for dialog, result in zip(dialogs, results):
        for msg in dialog:
            print(f"{msg['role'].capitalize()}: {msg['content']}\n")
        print(
            f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
        )

    if len(results) > 0:
        utterance = results[0]["generation"]["content"]
    else:
        utterance = ""

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
