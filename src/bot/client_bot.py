import threading

from tts import say
from stt import listen
from brain.client_brain import think
from statemachine import StateMachine, State
from pynput.keyboard import Key, Listener


class ClientBot(StateMachine):
    idle = State(name="idle", initial=True)
    listening = State(name="listening")
    responding = State(name="responding")
    cycle = idle.to(listening) | listening.to(responding) | responding.to(idle)

    def __init__(self) -> "ClientBot":
        super().__init__()

        self.__last_heard_utterance = None
        self.__last_thought_utterance = None
        self.__must_listen = False

    def live(self):
        def __on_press(key):
            if key != Key.space:
                return True

            if self.__must_listen:
                return True

            if self.current_state.id == "idle":
                self.__must_listen = True
                self.cycle()

            return True

        def __on_release(key):
            if key != Key.space:
                return True

            if not self.__must_listen:
                return True

            if self.current_state.id == "listening":
                self.__must_listen = False

            return True

        listener = Listener(on_press=__on_press, on_release=__on_release)
        listener.start()

        while True:
            pass

    def on_enter_idle(self):
        print("I am waiting")

    def on_exit_idle(self):
        print("I am not waiting anymore")

    def on_enter_listening(self):
        print("I am listening")

        def __should_listen() -> bool:
            return self.__must_listen

        def __start_listening():
            self.__last_heard_utterance = listen(__should_listen)
            self.cycle()

        thread = threading.Thread(target=__start_listening)
        thread.start()

    def on_exit_listening(self):
        print("I am not listening anymore")

    def on_enter_responding(self):
        print("I am responding about", self.__last_heard_utterance)

        def __on_new_sentence(utterance: str):
            say(utterance)

        self.__last_said_utterance = think(
            self.__last_heard_utterance, on_new_sentence=__on_new_sentence
        )
        print(self.__last_said_utterance)
        self.cycle()

    def on_exit_responding(self):
        print("I am not responding anymore")
        self.__last_heard_utterance = None
        self.__last_said_utterance = None
