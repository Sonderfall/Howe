import webbrowser
import os

from pynput.keyboard import Key, Controller
from fire import Fire
from http.server import HTTPServer, SimpleHTTPRequestHandler, test


DIRECTORY = None


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_no_cache_headers()
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPRequestHandler.end_headers(self)

    def send_no_cache_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")


def serve(directory: str = None):
    global DIRECTORY
    DIRECTORY = directory

    test(
        CORSRequestHandler,
        HTTPServer,
        port=8000,
    )


def play_in_browser():
    keyboard = Controller()
    with keyboard.pressed(Key.ctrl_l):
        keyboard.press("w")
        keyboard.release("w")

    absp = os.path.abspath("resources/wave.html")
    path = f"file:///{absp}"

    webbrowser.open(path, new=0)


if __name__ == "__main__":
    Fire(serve)
