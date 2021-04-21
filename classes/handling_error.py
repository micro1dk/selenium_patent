from functools import wraps

class HandlingError:
    def __init__ (self, err_msg, is_raise=False):
        self.err_msg = err_msg
        self.is_raise = is_raise

    def __call__ (self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                func(*args, **kwargs)
                return True
            except Exception as e:
                if self.is_raise:
                    raise Exception(f'{self.err_msg}: {e}')
                print(f'{self.err_msg}: {e}')
                return False
        return decorator
