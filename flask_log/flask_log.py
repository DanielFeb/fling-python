import logging
import multiprocessing
from queue import Full
from random import random
from time import sleep

from flask import Flask

from config.base import configuration
from executor.executor import MultiProcessExecutor, ProcessPoolExecutor
from executor.task import Task
from ilogging import logconfig


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
        executor.add_task(Task(hello, args={
            "name": name,
            "greet": greet
        }, unique_key=name, pre_process=change_args))
        app.logger.info("Start " + message)
    except Full:
        app.logger.warn("Server is busy: " + message)
        return 'Server is busy!'

    return 'Hello World!'


@app.route('/pool')
def pool():
    current_value = sequence.value
    sequence.increase()

    name = 'Pool' + str(current_value)
    greet = 'Hello' + str(current_value)
    message = "{0}, {1} !".format(greet, name)

    try:
        pool_executor.add_task(Task(hello, args={
            "name": name,
            "greet": greet
        }, unique_key=name, pre_process=change_args))
        app.logger.info("Start " + message)
    except Full:
        app.logger.warn("Server is busy: " + message)
        return 'Server is busy!'

    return 'Hello World!'


def change_args(task):
    task.get_args()["greet"] += "-tail"


def hello(args_dict):
    greet = args_dict["greet"]
    name = args_dict["name"]
    for i in range(100):
        logging.info("log " + name)
    if random() > 0.5:
        message = "Should timeout {1}!".format(multiprocessing.current_process().name, greet, name)
        logging.warning(message)
        sleep(5)
    else:
        sleep(3)
    message = "{0}, End {1}, {2} !".format(multiprocessing.current_process().name, greet, name)
    logging.info(message)


@app.errorhandler(404)  #当报错是404的时候就走这个函数
def handle_bad_request(e):
    # return 'bad request!', 400
    return "The resource is missing"

if __name__ == '__main__':
    multiprocessing.freeze_support()
    logconfig.enable()
    executor = MultiProcessExecutor(configuration.get("executor.queue_size", 0),
                                    configuration.get("executor.concurrent_count", 1),
                                    configuration.get("executor.timeout", 2))
    pool_executor = ProcessPoolExecutor(configuration.get("executor.queue_size", 0),
                                        configuration.get("executor.concurrent_count", 2))

    executor.start()
    pool_executor.start()
    app.run()
    executor.stop()
    pool_executor.stop()
