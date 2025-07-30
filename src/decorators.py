import time
from typing import Callable


def time_of_function(func: Callable):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        execution_time = round(time.time() - start, 4)
        print(f'execution time {execution_time}')
        return res
    return wrapper
