from controller.test import test_blu


@test_blu.route('/hello')
def helloTest():
    return "hello test!!"
