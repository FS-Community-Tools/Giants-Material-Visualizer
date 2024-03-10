import logging


def print(*args):
    msg = ' '.join(map(str, args))
    logging.log(logging.WARNING, msg)
