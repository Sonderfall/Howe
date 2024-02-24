from dataclasses import dataclass
from dataclasses_json import dataclass_json
from brain.server_memory import get_knowledge
from openai import OpenAI


__history = [
    {"role": "system", "content": get_knowledge()},
]


@dataclass_json
@dataclass
class _OpenAICOnfig:
    api_key: str
    organization_id: str


def _config_from_file(config_filepath: str) -> _OpenAICOnfig:
    with open(config_filepath, "rb") as f:
        config = _OpenAICOnfig.from_json(f.read())

    return config


__client_config = _config_from_file("config/openai.json")
__client = OpenAI(
    api_key=__client_config.api_key, organization=__client_config.organization_id
)


def think(utterance: str, on_new_sentence: callable = None) -> str:
    __history.append({"role": "user", "content": utterance})

    response = __client.chat.completions.create(
        model="gpt-3.5-turbo-0125", messages=__history
    )

    ret = response.choices[0].message
    content = ret.content

    __history.append({"role": "system", "content": content})

    if on_new_sentence is not None:
        on_new_sentence(content)

    return content


if __name__ == "__main__":

    def __test(utterance: str):
        import time

        print("Question:", utterance)
        print("Reponse:", think(utterance=utterance))
        print("===============================")

        time.sleep(2)

    __test("Qui es tu ?")
    __test("Quelle année sommes nous ?")
    __test("Depuis quand le vaisseau est il arrété ?")
    __test("Où es le capitaine ?")
    __test("Pourquoi le vaisseau s'est arrété ?")
    __test("Que peux tu me dire sur le vaisseau ?")
    __test("Que doit on faire pour que le vaisseau redémarre ?")
