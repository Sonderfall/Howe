from sqs import ThinkRequest, ThinkResponse
from threading import Thread
from brain.server_memory import get_knowledge

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    TextIteratorStreamer,
)


# __MODEL_NAME = "TheBloke/Vigostral-7B-Chat-GPTQ"
# __MODEL_NAME = "bofenghuang/vigostral-7b-chat"
# https://github.com/bofenghuang/vigogne
# __REVISION = "main"
# __REVISION = "gptq-8bit-32g-actorder_True" ## crash
__MODEL_NAME = "bofenghuang/vigogne-2-7b-chat"
__REVISION = "v2.0"

__model = AutoModelForCausalLM.from_pretrained(
    __MODEL_NAME, revision=__REVISION, device_map="cuda:0"
)
__tokenizer = AutoTokenizer.from_pretrained(
    __MODEL_NAME, revision=__REVISION, use_fast=True
)
__streamer = TextIteratorStreamer(
    __tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True
)
__history = []
__knowledge = get_knowledge()


def think(request: ThinkRequest, on_new_word: callable) -> str:
    response = __chat(
        query=request.utterance,
        temperature=request.temperature,
        max_new_tokens=request.max_len,
        on_new_word=on_new_word,
        top_k=request.top_k,
        top_p=request.top_p,
        use_cache=False,
    )

    print(response)

    return response


def __chat(
    query: str,
    temperature: float = 0.7,
    on_new_word: callable = None,
    top_p: float = 1.0,
    top_k: float = 0,
    repetition_penalty: float = 1.1,
    max_new_tokens: int = 256,
    **kwargs,
):
    global __history
    if __history is None:
        __history = []

    __history.append({"role": "user", "content": query})

    input_ids = __tokenizer.apply_chat_template(
        conversation=__history,
        add_generation_prompt=True,
        return_tensors="pt",
        chat_template=__knowledge,
    ).to(__model.device)

    def __generate():
        _ = __model.generate(
            input_ids=input_ids,
            generation_config=GenerationConfig(
                temperature=temperature,
                do_sample=temperature > 0.0,
                top_p=top_p,
                top_k=top_k,
                repetition_penalty=repetition_penalty,
                max_new_tokens=max_new_tokens,
                pad_token_id=__tokenizer.eos_token_id,
                **kwargs,
            ),
            streamer=__streamer,
            return_dict_in_generate=True,
        )

    Thread(target=__generate).start()

    whole_utterance = ""
    current_sentence = ""

    for new_text in __streamer:
        current_sentence += new_text

        if (
            "." in new_text
            or "?" in new_text
            or "!" in new_text
            or ";" in new_text
            or ":" in new_text
        ):
            if on_new_word is not None:
                on_new_word(ThinkResponse(utterance=current_sentence, end=False))

            whole_utterance += current_sentence
            current_sentence = ""

    if on_new_word is not None:
        on_new_word(ThinkResponse(utterance="", end=True))

    __history.append({"role": "assistant", "content": whole_utterance})

    return whole_utterance


if __name__ == "__main__":
    default_top_k = 15
    default_top_p = 1
    default_max_len = 512
    default_temp = 1

    print(
        think(
            ThinkRequest(
                utterance="Qui es tu ?",
                temperature=default_temp,
                max_len=default_max_len,
                top_k=default_top_k,
                top_p=default_top_p,
            )
        )
    )

    print(
        think(
            ThinkRequest(
                utterance="Quelle année sommes nous ?",
                temperature=default_temp,
                max_len=default_max_len,
                top_k=default_top_k,
                top_p=default_top_p,
            )
        )
    )

    print(
        think(
            ThinkRequest(
                utterance="Depuis quand le vaisseau est il arrété ?",
                temperature=default_temp,
                max_len=default_max_len,
                top_k=default_top_k,
                top_p=default_top_p,
            )
        )
    )

    print(
        think(
            ThinkRequest(
                utterance="Où es le capitaine ?",
                temperature=default_temp,
                max_len=default_max_len,
                top_k=default_top_k,
                top_p=default_top_p,
            )
        )
    )

    print(
        think(
            ThinkRequest(
                utterance="Pourquoi le vaisseau s'est arrété ?",
                temperature=default_temp,
                max_len=default_max_len,
                top_k=default_top_k,
                top_p=default_top_p,
            )
        )
    )

    print(
        think(
            ThinkRequest(
                utterance="Que peux tu me dire sur le vaisseau ?",
                temperature=default_temp,
                max_len=default_max_len,
                top_k=default_top_k,
                top_p=default_top_p,
            )
        )
    )

    print(
        think(
            ThinkRequest(
                utterance="Que doit on faire pour que le vaisseau redémarre ?",
                temperature=default_temp,
                max_len=default_max_len,
                top_k=default_top_k,
                top_p=default_top_p,
            )
        )
    )
