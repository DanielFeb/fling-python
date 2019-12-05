class Task():
    def __init__(self, func, args, unique_key="No-Name-Task") -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.unique_key = unique_key

    def run(self):
        self.func(**self.args)
