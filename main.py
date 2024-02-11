from bot import ClientBot, ServerBot
from fire import Fire


def main(mode: str = "client"):
    bot = None

    if mode == "client":
        bot = ClientBot()
    elif mode == "server":
        bot = ServerBot()

    if bot == None:
        print("Unknown mode:", mode)
        return

    bot.live()


if __name__ == "__main__":
    Fire(main)
