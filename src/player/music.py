import time
import os

from pygame import mixer


def play(filepath: str, should_continue: callable = None, loop: bool = False):
    if filepath is None or not os.path.exists(filepath):
        return

    mixer.init()
    mixer.music.load(filepath)

    if loop:
        mixer.music.play(loops=9999)
    else:
        mixer.music.play()

    while mixer.music.get_busy():  # wait for music to finish playing
        if should_continue is not None and not should_continue():
            mixer.music.stop()
            break

        time.sleep(0.1)
