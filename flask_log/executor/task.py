class Task():
    def __init__(self, func, args=(), unique_key="No-Name-Task") -> None:
        super().__init__()
        self._func = func
        self._args = args
        self.unique_key = unique_key

    def run(self):
        self._func(*self._args)

    def get_func(self):
        return self._func

    def get_args(self):
        return self._args
