from fire import Fire


def _start_client():
    from bot.client_bot import ClientBot

    bot = ClientBot()

    bot.live()


def _start_server():
    from bot.server_bot import ServerBot

    bot = ServerBot()

    bot.live()


def _spawn_server():
    from spawner.scaleway_spawner import spawn

    spawn()


def _kill_server():
    from spawner.scaleway_spawner import kill

    kill()


class Main(object):
    def run(self, mode: str = "client"):
        print("Starting in", mode, "mode")

        if mode == "client":
            _start_client()
        elif mode == "server":
            _start_server()
        else:
            print("Unknown mode:", mode)

    def spawn(self):
        _spawn_server()

    def kill(self):
        _kill_server()


if __name__ == "__main__":
    Fire(Main)
