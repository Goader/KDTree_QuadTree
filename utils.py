import numpy as np
import time
from functools import wraps


def get_numpy_type(array):
    for i in range(len(array)):
        if isinstance(array[i], (float, np.float32, np.float64)):
            return np.float64
    return np.int64


def timeit(title, precision):
    assert len(title) <= 26, 'Title length must not exceed 26 characters'

    def inner_decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            t = time.time() - t0
            tabs = '\t' * ((26 - len(title)) // 4)
            print(f'{title}:{tabs}{round(t, precision)}')
            return result
        return inner
    return inner_decorator
