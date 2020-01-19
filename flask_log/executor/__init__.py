from config.base import configuration
from executor.executor import MultiProcessExecutor, ProcessPoolExecutor

if configuration.get("executor", None) is not None:
    executor = MultiProcessExecutor(configuration.get("executor.queue_size", 0),
                                    configuration.get("executor.concurrent_count", 1),
                                    configuration.get("executor.timeout", 2))
    pool_executor = ProcessPoolExecutor(configuration.get("executor.queue_size", 0),
                                        configuration.get("executor.concurrent_count", 2))