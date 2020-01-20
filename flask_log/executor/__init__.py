from config.base import configuration
from executor.executor import MultiProcessExecutor, ProcessPoolExecutor

executor = None
pool_executor = None
if configuration.get("executor", None) is not None:
    executor = MultiProcessExecutor(configuration.get("executor.queueSize", 0),
                                    configuration.get("executor.concurrentCount", 1),
                                    configuration.get("executor.timeout", 2))
    pool_executor = ProcessPoolExecutor(configuration.get("executor.queueSize", 0),
                                        configuration.get("executor.concurrentCount", 2))
