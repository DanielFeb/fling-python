import logging
import multiprocessing
import threading
from multiprocessing import Pool
from queue import Empty
from queue import Queue

from executor.task import Task


class SingleThreadExecutor():
    def __init__(self, queue_size=0) -> None:
        super().__init__()
        self.task_queue = Queue(queue_size)
        self.is_running = True

    def add_task(self, task):
        if self.is_running:
            self.task_queue.put(task, block=False)
        else:
            raise RuntimeError("Executor is stopped")

    def start(self):
        thread = threading.Thread(target=self.do_start, args=(self,))
        thread.start()

    def stop(self):
        self.is_running = False
        self.task_queue.put(Task(self.exit_task, unique_key="Final-Mission"), block=False)

    @staticmethod
    def exit_task():
        logging.info("Executor's Final Mission complete success!")

    def execute(self, task):
        task.run()

    @staticmethod
    def do_start(executor):

        while executor.is_running:
            task = executor.task_queue.get(block=True)
            executor.execute(task)

        try:
            task = executor.task_queue.get(block=False)
            logging.info("Executor is abandoned with unprocessed tasks!")
            while True:
                logging.info("Task {0} is not processed!".format(task.unique_key))
                try:
                    task = executor.task_queue.get(block=False)
                except Empty:
                    break
        except Empty:
            pass


class MultiThreadExecutor(SingleThreadExecutor):
    def __init__(self, queue_size=0, max_concurrent_count=1) -> None:
        super().__init__(queue_size)
        self._semaphore = threading.Semaphore(max_concurrent_count)

    def execute(self, task):
        self._semaphore.acquire()
        self.concurrent_execute(task)
        self._semaphore.release()

    def concurrent_execute(self, task):
        task.run()


class MultiProcessExecutor(MultiThreadExecutor):
    def __init__(self, queue_size=0, max_concurrent_count=1, timeout=None) -> None:
        super().__init__(queue_size, max_concurrent_count)
        self._timeout = timeout

    def concurrent_execute(self, task):
        process_name = multiprocessing.current_process().name
        logging.debug("Process {0} start with task {1}!".format(process_name, task.unique_key))
        p = Pool(1)
        res = p.apply_async(task.get_func(), task.get_args())
        p.close()
        try:
            res.get(self._timeout)  # Wait timeout seconds for func to complete.
            logging.debug("Success! Process {0} exit with task {1}!".format(process_name, task.unique_key))
        except multiprocessing.TimeoutError:
            message = "Timeout! Process {0} exit with task {1}".format(process_name, task.unique_key)
            logging.error(message)
            p.terminate()
        finally:
            p.terminate()
