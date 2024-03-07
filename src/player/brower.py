import webbrowser

from fire import Fire

def main():
    webbrowser.get("firefox").open("index.html", new = 0)

if __name__ == "__main__":
    Fire(main)