from queue import Full
from time import sleep

from flask import Flask
from config import logconfig
from config.base import configuration
from executor.executor import Executor
from executor.task import Task

logconfig.enable()

executor = Executor(configuration.get_optional_property_with_default("executor.queue_size", 0))


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
        executor.add_task(Task(hello, {
            'name': name,

            'greet': greet
        }, unique_key=name))
        app.logger.info("Start " + message)
    except Full:
        app.logger.warn("Server is busy: " + message)
        return 'Server is busy!'

    return 'Hello World!'


def hello(name, greet):
    sleep(3)
    message = "End {0}, {1} !".format(greet, name)
    app.logger.info(message)


if __name__ == '__main__':
    executor.start()
    app.run()
    executor.stop(drop=True)
