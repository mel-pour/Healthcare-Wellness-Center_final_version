from functools import wraps

from utils.logger import logger


def handle_errors(method):
    """Catches any error in a controller method, logs it, and returns (False, message)."""

    @wraps(method)  # keeps the original method's name, which the log message uses
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except ValueError as e:
            # A broken rule, such as "Customer not found."
            logger.warning(f"{method.__qualname__}: {e}")
            return False, f"Error : {e}"
        except Exception as e:
            # Something unexpected, such as a missing data file. The full traceback is logged.
            logger.exception(f"Unexpected error in {method.__qualname__}")
            return False, f"Error : {e}"

    return wrapper
