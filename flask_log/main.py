import multiprocessing

from flask import Flask

from controller.logging import logging_blu
from controller.test import test_blu
from executor import executor, pool_executor
from ilogging import logconfig

app = Flask(__name__)
app.register_blueprint(test_blu, url_prefix="/test")
app.register_blueprint(logging_blu, url_prefix="/log")

if __name__ == '__main__':

    executor.start()
    pool_executor.start()
    multiprocessing.freeze_support()
    logconfig.enable()
    app.run()
    executor.stop()
    pool_executor.stop()
