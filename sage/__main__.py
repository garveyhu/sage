import threading

import uvicorn

from sage.api.main import app


def run_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=8000)


def load_thread(app_function):
    thread = threading.Thread(target=app_function)
    thread.start()
    return thread


def main(apps):
    threads = [load_thread(app) for app in apps]

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    run_uvicorn()
