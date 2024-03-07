#!/usr/bin/env python3
from fire import Fire
from http.server import HTTPServer, SimpleHTTPRequestHandler, test


DIRECTORY = None


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPRequestHandler.end_headers(self)


def main(directory : str = None):
    global DIRECTORY
    DIRECTORY = directory

    test(
        CORSRequestHandler,
        HTTPServer,
        port=8000,
    )


if __name__ == "__main__":
    Fire(main)