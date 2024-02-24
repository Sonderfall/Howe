from dataclasses import dataclass
from dataclasses_json import dataclass_json
from sqs import ThinkRequest
from brain.server_memory import get_knowledge
from openai import OpenAI


__history = [
    {"role": "system", "content": get_knowledge()},
]


@dataclass_json
@dataclass
class _OpenAICOnfig:
    api_key: str


def _config_from_file(config_filepath: str) -> _OpenAICOnfig:
    with open(config_filepath, "rb") as f:
        config = _OpenAICOnfig.from_json(f.read())

    return config


__client = OpenAI(api_key=_config_from_file("config/openai.json").api_key)


def think(request: ThinkRequest, on_new_sentence: callable = None) -> str:
    response = __chat(query=request.utterance, on_new_sentence=on_new_sentence)

    return response


def __chat(query: str, **kwargs):
    # global __history
    # if __history is None:
    #     __history = []

    __history.append({"role": "user", "content": query})

    response = __client.chat.completions.create(
        model="gpt-3.5-turbo-0125", messages=__history
    )

    return response.choices[0].message


def __test(utterance: str):
    import time

    default_top_k = 25
    default_top_p = 2
    default_max_len = 512
    default_temp = 0.7

    print("Question:", utterance)
    print(
        "Reponse:",
        think(
            ThinkRequest(
                utterance=utterance,
                temperature=default_temp,
                max_len=default_max_len,
                top_k=default_top_k,
                top_p=default_top_p,
            )
        ),
    )
    print("===============================")
    time.sleep(5)


if __name__ == "__main__":
    # print(__knowledge)
    __test("Qui es tu ?")
    __test("Quelle année sommes nous ?")
    __test("Depuis quand le vaisseau est il arrété ?")
    __test("Où es le capitaine ?")
    __test("Pourquoi le vaisseau s'est arrété ?")
    __test("Que peux tu me dire sur le vaisseau ?")
    __test("Que doit on faire pour que le vaisseau redémarre ?")
