import os

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from brain.knowledge import get_knowledge
from openai import OpenAI

__SAVE_FILE = "tmp/history.json"


@dataclass_json
@dataclass
class __OpenAIConfig:
    api_key: str
    organization_id: str


@dataclass_json
@dataclass
class __SavedState:
    step: str
    history: list


def __save(state: __SavedState):
    dir = os.path.dirname(__SAVE_FILE)

    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(__SAVE_FILE, "w") as out:
        out.write(state.to_json())


def __load() -> __SavedState:
    if not os.path.exists(__SAVE_FILE):
        step_state = 0
        return __SavedState(
            history=[{"role": "system", "content": get_knowledge(step_state)}],
            step=step_state,
        )

    with open(__SAVE_FILE, "r") as f:
        state = __SavedState.from_json(f.read())

    return state


def __config_from_file(config_filepath: str) -> __OpenAIConfig:
    with open(config_filepath, "rb") as f:
        config = __OpenAIConfig.from_json(f.read())

    return config


__client_config = __config_from_file("config/openai.json")
__client = OpenAI(
    api_key=__client_config.api_key, organization=__client_config.organization_id
)


def think(utterance: str, on_new_sentence: callable = None) -> str:
    state = __load()

    state.history.append({"role": "user", "content": utterance})

    response = __client.chat.completions.create(
        model="gpt-3.5-turbo-0125", messages=state.history
    )

    ret = response.choices[0].message
    content = ret.content

    state.history.append({"role": "system", "content": content})
    content = content.replace(",", "")

    __save(state)

    return content


if __name__ == "__main__":

    def __test(utterance: str):
        import time

        print("Question:", utterance)
        resp = think(utterance=utterance)
        print("Reponse:", resp)
        print("===============================")

        time.sleep(2)

    __test("Qui es tu ?")
    __test("Que sais tu de la compagnie ?")
    __test("Quelle année sommes nous ?")
    __test("Depuis quand le vaisseau est il arrété ?")
    __test("Où es le capitaine ?")
    __test("Pourquoi le vaisseau s'est arrété ?")
    __test("Que peux tu me dire sur le vaisseau ?")
    __test("Que doit on faire pour que le vaisseau redémarre ?")
