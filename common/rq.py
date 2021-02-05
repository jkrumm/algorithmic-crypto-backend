from rq import Queue
from flask import current_app

QUEUE_NAME_DEFAULT = "default"
QUEUE_NAME_HIGH = "high"
QUEUE_NAME_MEDIUM = "medium"
QUEUE_NAME_LOW = "low"


class RQ:
    def __init__(
        self,
        initialize_queue=True,
        is_async=True,
        queue_name=QUEUE_NAME_DEFAULT,
        cache=None,
    ):
        self._queue_name = queue_name
        self._is_async = is_async
        self._cache = cache if cache else current_app.cache
        if initialize_queue:
            self.queue(queue_name=QUEUE_NAME_DEFAULT, is_async=self._is_async)

    def queue(self, queue_name=QUEUE_NAME_DEFAULT, is_async=True):
        self._queue = Queue(queue_name, is_async=is_async, connection=self._cache)
        return self

    def enqueue(self, func, func_params=None, ttl=None):
        return self._queue.enqueue(func, ttl=ttl, kwargs=func_params)

    def get_result_by_job_id(self, job_id):
        result = self._queue.fetch_job(job_id)
        return result.result if result else None

    def empty(self):
        return self._queue.empty()
