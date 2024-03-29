import os
import hashlib
import time

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
    step: int
    history: list
    hash: str

    @property
    def compute_hash(self) -> str:
        s = f"{self.history}+{self.step}"
        return hashlib.sha256(s.encode()).hexdigest()


def __save(state: __SavedState):
    dir = os.path.dirname(__SAVE_FILE)

    if not os.path.exists(dir):
        os.makedirs(dir)

    state.hash = state.compute_hash

    with open(__SAVE_FILE, "w") as out:
        out.write(state.to_json())


def __load() -> __SavedState:
    state = None

    if not os.path.exists(__SAVE_FILE):
        state = __SavedState(
            step=0, history=[{"role": "system", "content": get_knowledge(0)}], hash=None
        )
    else:
        with open(__SAVE_FILE, "r") as f:
            state = __SavedState.from_json(f.read())

    if state.hash is not None and state.compute_hash != state.hash:
        print("New computed hash, updating knowledge...")

        if state.step > 0:
            state.history.append(
                {"role": "system", "content": get_knowledge(state.step)}
            )

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

    def __call_api():
        try:
            response = __client.chat.completions.create(
                model="gpt-3.5-turbo-0125", messages=state.history
            )
            return response.choices[0].message.content
        except Exception as e:
            print("Error with OpenAI", str(e))
            time.sleep(3)
            return __call_api()

    content = __call_api()
    state.history.append({"role": "system", "content": content})
    content = content.replace(",", "")

    __save(state)

    return content


if __name__ == "__main__":
    def __test(utterance: str):
        print("Question:", utterance)
        resp = think(utterance=utterance)
        print("Reponse:", resp)
        print("===============================")

        time.sleep(2)

    __test("Quels sont les résultats du scan ?")
    # __test("Qui es tu ?")
    # __test("Que sais tu de la compagnie ?")
    # __test("Quelle année sommes nous ?")
    __test(
        "On cherche des hydrocarbures, de type alcyne, sur quelle planète pourrait on en trouver ?"
    )
    # __test("Depuis quand le vaisseau est il arrété ?")
    __test("Où es le capitaine ?")
    __test("Pourquoi le vaisseau s'est arrété ?")
    # __test("Que peux tu me dire sur le vaisseau ?")
    __test("Que doit on faire pour que le vaisseau redémarre ?")
