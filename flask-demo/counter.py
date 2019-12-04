import time


class Counter:
    def __init__(self, value=0):
        self.currentValue = value
        self.isRunning = True

    def stop(self):
        self.isRunning = False

    def run(self):
        self.isRunning = True

    def process(self):
        self.currentValue = self.currentValue + 1
        time.sleep(1)
        return self.currentValue
