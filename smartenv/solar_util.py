import requests
import time
from functools import lru_cache, wraps

BASE_URL = "https://api.solcast.com.au/world_radiation/estimated_actuals"
API_KEY = "Ed2ld1UasQQmaO1Uju1ssFGRQRvfKyjP"  
RETRY_COUNT = 3
DELAY_SECONDS = 60
CACHE_DURATION = 3600  # 1 hour in seconds

def cache_with_timeout(timeout):
    """Decorator to clear cache of a function after a certain timeout."""
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            current_time = time.time()
            if current_time - wrapped.last_called >= timeout:
                wrapped.cache_clear()
            wrapped.last_called = current_time
            return fn(*args, **kwargs)
        wrapped.cache_clear = lru_cache(maxsize=None)(fn).cache_clear
        wrapped.last_called = time.time()
        return wrapped
    return decorator

@cache_with_timeout(CACHE_DURATION)
@lru_cache(maxsize=None)
def get_solar_irradiance(latitude=25, longitude=13):
    """... (rest of the function as before) ..."""

if __name__ == "__main__":
    # Test the function
    data = get_solar_irradiance()
    print(data)
