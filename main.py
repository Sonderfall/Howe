import fire

from ai import Assistant


def main():
    assistant = Assistant()
    assistant.live()


if __name__ == "__main__":
    fire.Fire(main)
