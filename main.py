from fire import Fire


def __start_client():
    from bot.client_bot import ClientBot

    bot = ClientBot()

    bot.live()


def __start_server():
    from bot.server_bot import ServerBot

    bot = ServerBot()

    bot.live()


def main(mode: str = "client"):
    print("Starting in", mode, "mode")

    if mode == "client":
        __start_client()
    elif mode == "server":
        __start_server()


if __name__ == "__main__":
    Fire(main)
