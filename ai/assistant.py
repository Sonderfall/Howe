import threading

from tts import say
from stt import listen
from statemachine import StateMachine, State
from pynput.keyboard import Key, Listener


class Assistant(StateMachine):
    idle = State(name="idle", initial=True)
    listening = State(name="listening")
    thinking = State(name="thinking")
    speaking = State(name="speaking")
    cycle = (
        idle.to(listening)
        | listening.to(thinking)
        | thinking.to(speaking)
        | speaking.to(idle)
    )

    def __init__(self) -> "Assistant":
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
            self.__last_heard_utterance = None
            self.__last_heard_utterance = listen(__should_listen)
            self.cycle()

        thread = threading.Thread(target=__start_listening)
        thread.start()

    def on_exit_listening(self):
        print("I am not listening anymore")

    def on_enter_thinking(self):
        print("I am thinking about", self.__last_heard_utterance)
        self.__last_thought_utterance = None
        self.__last_thought_utterance = self.__last_heard_utterance
        self.cycle()

    def on_exit_thinking(self):
        print("I am not thinking anymore")

    def on_enter_speaking(self):
        print("I am speaking")
        say(self.__last_thought_utterance)
        self.cycle()

    def on_exit_speaking(self):
        print("I am not speaking anymore")
        self.__last_thought_utterance = None
