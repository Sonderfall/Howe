from tts import say
from stt import listen
from statemachine import StateMachine, State
from pynput.keyboard import Key, Listener

class Assistant(StateMachine):
    idle_state = State(name="idle", initial=True)
    listening_state = State(name="listening")
    thinking_state = State(name="thinking")
    speaking_state = State(name="speaking")
    cycle = (
        idle_state.to(listening_state)
        | listening_state.to(thinking_state)
        | thinking_state.to(speaking_state)
        | speaking_state.to(idle_state)
    )

    def __init__(self) -> "Assistant":
        super().__init__()

        self.__last_heard_utterance = None
        self.__last_thought_utterance = None
        self.__must_listen = False

    def live(self):
        def on_press(key):
            if key != Key.space:
                return

            if self.__must_listen:
                return

            if self.current_state.id == "idle":
                self.__must_listen = True
                self.cycle()

        def on_release(key):
            if key != Key.space:
                return

            if not self.__must_listen:
                return
        
            if self.current_state.id == "listening":
                self.__must_listen = False
                self.cycle()

        self.cycle()

        listener = Listener(
                on_press=on_press,
                on_release=on_release)
        listener.start()

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
