"""Demonic decorator."""
from multiprocessing import Process

def daemon(func):
    def wrapper(*args):
        daemon = Process(
            target = func,
            args = list(args),
            daemon = True
        )
        daemon.start()
    return wrapper
