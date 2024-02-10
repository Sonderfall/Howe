import keyboard

from tts import say
from stt import listen
from statemachine import StateMachine, State


class Assistant(StateMachine):
    def __init__(self) -> "Assistant":
        self.__IdleState = State(name="idle", initial=True)
        self.__ListeningState = State(name="listening")
        self.__ThinkingState = State(name="thinking")
        self.__SpeakingState = State(name="speaking")
        self.__cycle = (
            self.__IdleState.to(self.__ListeningState)
            | self.__ListeningState.to(self.__ThinkingState)
            | self.__ThinkingState.to(self.__SpeakingState)
            | self.__SpeakingState.to(self.__IdleState)
        )

        self.__last_heard_utterance = None
        self.__last_thought_utterance = None
        self.__must_listen = False
        self.__hotkey = "space"

    def live(self):
        def on_press():
            if self.current_state.id == "idle":
                self.__must_listen = True
                self.__cycle()

        def on_release():
            if self.current_state.id == "listening":
                self.__must_listen = False
                self.__cycle()

        keyboard.on_press_key(self.__hotkey, on_press)
        keyboard.on_release_key(self.__hotkey, on_release)

        while True:
            pass

    def on_enter_idle(self):
        print("I am waiting")

    def on_exit_idle(self):
        print("I am not waiting anymore")

    def on_enter_listening(self):
        print("I am listening")

        def should_listen() -> bool:
            return self.__must_listen

        self.__last_heard_utterance = None
        self.__last_heard_utterance = listen(should_listen)
        # self.__cycle()

    def on_exit_listening(self):
        print("I am not listening anymore")

    def on_enter_thinking(self):
        print("I am thinking about", self.__last_heard_utterance)
        self.__last_thought_utterance = None
        self.__last_thought_utterance = "Je ne suis pas d'accord"
        self.__cycle()

    def on_exit_thinking(self):
        print("I am not thinking anymore")

    def on_enter_speaking(self):
        print("I am speaking")
        say(self.__last_thought_utterance)
        self.__cycle()

    def on_exit_speaking(self):
        print("I am not speaking anymore")
        self.__last_thought_utterance = None
