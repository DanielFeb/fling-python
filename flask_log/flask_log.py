from flask import Flask
from config import logconfig


logconfig.enable()

app = Flask(__name__)


@app.route('/')
def hello_world():
    app.logger.info("hello")
    return 'Hello World!'


# @app.teardown_appcontext
# def teardown_appcontext():
#
#     app.logger.info("shut down!")
#     print("shut down!")


if __name__ == '__main__':
    app.run()
