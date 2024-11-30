from functools import wraps
from loguru import logger
import time

def listen(retries=3, backoff=0.5):
    def decorator(func):
        @wraps(func)
        def attempt(*args, **kwargs):
            i = 0
            wait = backoff
            while i < retries:
                result = func(*args, **kwargs)
                if result:
                    return result
                logger.warning(f"Retrying {func.__name__} in {wait} seconds because attempt {i+1} failed with result {result}")
                time.sleep(wait)
                i += 1
                wait *= 2
            logger.error(f"Failed to get result from {func.__name__} after {retries} attempts, returning None")
            return None
        return attempt
    return decorator

def hex2str(hex):
    return bytes.fromhex(hex[2:]).decode("utf-8")


def str2hex(str):
    return "0x" + str.encode("utf-8").hex()
