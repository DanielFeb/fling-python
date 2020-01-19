from flask import Blueprint

logging_blu = Blueprint("logging", __name__)

from controller.logging.hello import *