from flask import Blueprint

test_blu = Blueprint("test", __name__)

from controller.test.hello import *

