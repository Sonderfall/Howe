import time

from statemachine import StateMachine, State
from sqs import respond, wait_request, ThinkResponse
from brain.openai_server_brain import think


class ServerBot(StateMachine):
    idle = State(name="idle", initial=True)
    responding = State(name="responding")

    cycle = idle.to(responding) | responding.to(idle)

    def __init__(self) -> "ServerBot":
        super().__init__()
        self.__last_heard_utterance = None

    def live(self):
        while True:
            time.sleep(10)

    def on_enter_idle(self):
        print("I am waiting")
        self.__last_heard_utterance = wait_request().utterance
        self.cycle()

    def on_exit_idle(self):
        print("I am not waiting anymore")

    def on_enter_responding(self):
        print("I am responding about", self.__last_heard_utterance)

        if self.__last_heard_utterance is not None:
            response = think(self.__last_heard_utterance)
            print(response)
            respond(ThinkResponse(utterance=response, end=True))

        self.cycle()

    def on_exit_responding(self):
        print("I am not responding anymore")
        self.__last_heard_utterance = None
