
import time
from contextlib import contextmanager
@contextmanager
def timer():
    t0 = time.perf_counter(); data = {}
    try: yield data
    finally: data['seconds'] = time.perf_counter() - t0
