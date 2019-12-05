import threading
from queue import Queue, Empty

import logging


class Executor():
    def __init__(self, queue_size=0) -> None:
        super().__init__()
        self.task_queue = Queue(queue_size)
        self.result_dict = Queue(queue_size)
        self.is_running = True
        self.is_dropped = False

    def add_task(self, task):
        if self.is_running:
            self.task_queue.put(task, block=False)
        else:
            raise RuntimeError("Executor is stopped")

    def start(self):
        thread = threading.Thread(target=self.do_start, args=(self,))
        thread.start()

    def stop(self, drop=False):
        self.is_running = False
        self.is_dropped = drop

    @staticmethod
    def do_start(executor):
        while executor.is_running:
            task = executor.task_queue.get(block=True)
            task.run()

        if executor.is_dropped:
            task = executor.task_queue.get(block=False)
            if task is not None:
                logging.info("Executor is abandoned with unprocessed tasks!")
            while True:
                logging.info("Task {0} is not processed!".format(task.unique_key))
                try:
                    task = executor.task_queue.get(block=False)
                except Empty:
                    break

