import logging
from functools import wraps

from fastapi import HTTPException

log_filename = "logger/logging.txt"


def log_decorator(func):
    @wraps(func)
    def inner_wrapper(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        message = returned_value
        print(type(message))
        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        if not isinstance(message, dict):
            message = {'msg': 'succeeded'}
        logging.info(str(func.__name__) + ' ' + str(message))
        return returned_value
    return inner_wrapper
