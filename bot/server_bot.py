from statemachine import StateMachine, State
from sqs import respond, wait_request, ThinkResponse
from brain import think_server


class ServerBot(StateMachine):
    idle = State(name="idle", initial=True)
    thinking = State(name="thinking")

    cycle = idle.to(thinking) | thinking.to(idle)

    def __init__(self) -> "ServerBot":
        super().__init__()
        self.__last_heard_utterance = None
        self.__last_thought_utterance = None

    def live(self):
        while True:
            pass

    def on_enter_idle(self):
        print("I am waiting")
        self.__last_heard_utterance = None
        self.__last_heard_utterance = wait_request()
        self.cycle()

    def on_exit_idle(self):
        print("I am not waiting anymore")

    def on_enter_thinking(self):
        print("I am thinking")
        self.__last_thought_utterance = think_server(self.__last_heard_utterance)
        respond(ThinkResponse(self.__last_thought_utterance))
        self.cycle()

    def on_exit_thinking(self):
        print("I am not thinking anymore")
        self.__last_thought_utterance = None
