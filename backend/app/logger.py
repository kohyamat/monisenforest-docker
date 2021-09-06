import logging
from logging.handlers import QueueHandler
from queue import Queue

log_queue = Queue(-1)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = QueueHandler(log_queue)
    logger.addHandler(handler)
    logger.addFilter(fmt_filter)
    return logger


def fmt_filter(rec):
    rec.levelname = "{}:".format(rec.levelname)
    return True
