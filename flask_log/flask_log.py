import multiprocessing
from queue import Full
from random import random
from time import sleep

from flask import Flask
from config import logconfig
from config.base import configuration
from executor.executor import SingleThreadExecutor, MultiProcessExecutor
from executor.task import Task

logconfig.enable()

executor = MultiProcessExecutor(configuration.get("executor.queue_size", 0),
                                configuration.get("executor.concurrent_count", 1),
                                configuration.get("executor.timeout", 2))


class Sequence():
    def __init__(self) -> None:
        super().__init__()

        self.value = 0

    def increase(self):
        self.value = self.value + 1

sequence = Sequence()

app = Flask(__name__)


@app.route('/')
def hello_world():
    current_value = sequence.value
    sequence.increase()

    name = 'Daniel' + str(current_value)
    greet = 'Hello' + str(current_value)
    message = "{0}, {1} !".format(greet, name)

    try:
        executor.add_task(Task(hello, args=(name, greet), unique_key=name))
        app.logger.info("Start " + message)
    except Full:
        app.logger.warn("Server is busy: " + message)
        return 'Server is busy!'

    return 'Hello World!'


def hello(name, greet):
    if random() > 0.5:
        message = "Should timeout {1}!".format(multiprocessing.current_process().name, greet, name)
        app.logger.warn(message)
        sleep(5)
    else:
        sleep(3)
    message = "{0}, End {1}, {2} !".format(multiprocessing.current_process().name, greet, name)
    app.logger.info(message)


if __name__ == '__main__':
    executor.start()
    app.run()
    executor.stop()
