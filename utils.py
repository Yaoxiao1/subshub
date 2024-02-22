import logging

class Scripts:
    def __init__(self, script_idx, time_period, content):
        self.script_idx = script_idx
        self.time_period = time_period
        self.content = content


def show_time_period(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        logging.info(f"{func.__name__} tooks {end-start} seconds to run!")
    return wrapper