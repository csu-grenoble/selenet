#
# SeleNet
#
# Authors : Nada Yassine, Meli Scott Douanla 
#

import time
from functools import wraps

def monitor_perf(func):
    """
    Decorator to monitor the perfermance of a function by measuring its execution time
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"[PERF] {func.__name__:<30} | Durée: {end_time - start_time:.4f}s")
        return result
    return wrapper