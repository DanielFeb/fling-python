
def echo(args):
    return args


class Task():
    def __init__(self, func, args={}, unique_key="No-Name-Task", pre_process=echo) -> None:
        super().__init__()
        self._func = func
        self._args = args
        self.unique_key = unique_key
        self._pre_process = pre_process

    def pre_process(self):
        self._pre_process(self)

    def run(self):
        self._func(self._args)

    def get_func(self):
        return self._func

    def get_args(self):
        return self._args

    def get_argument_tuple(self):
        return self._args,

