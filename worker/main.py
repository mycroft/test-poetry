#!/usr/bin/env python3

"""Some worker sample"""

import random
import threading
from time import sleep

from prometheus_client import Counter, Gauge, Histogram, start_http_server

from utils.consumer import MessageConsumer

WORKER_CREATED = Counter("worker_created_total", "Number of workers created")
WORKER_STARTED = Counter("worker_started_total", "Number of workers started")
WORKER_STOPPED = Counter("worker_stopped_total", "Number of workers stopped")
ACTIVE_WORKERS = Gauge("workers_active", "Number of active workers")
WORK_DURATION = Histogram(
    "worker_operation_duration_seconds", "Time spent on each work operation"
)


class Worker(threading.Thread):
    """Worker class"""

    def __init__(self, worker_id):
        """Worker constructor"""
        super().__init__()
        print(f"Worker created {worker_id}")
        self.stopped = False
        self.name = worker_id
        WORKER_CREATED.inc()
        ACTIVE_WORKERS.inc()

        self.consumer = MessageConsumer()

    def run(self):
        """Worker run method"""
        print("Worker running")
        WORKER_STARTED.inc()

        while not self.stopped:
            try:
                message = self.consumer.consume_one()
                if message is None:
                    continue

                print(f"Worker working {self.name} with message {message}")
                with WORK_DURATION.time():
                    sleep(random.randint(1, 5))

            except TimeoutError:
                pass

        self.consumer.close()

    def stop(self):
        """Stop the worker"""
        print(f"Worker stopped {self.name}")
        self.stopped = True
        WORKER_STOPPED.inc()
        ACTIVE_WORKERS.dec()

    def __str__(self) -> str:
        return "Worker"


class Engine:
    """Engine class"""

    def main(self):
        """Engine main method"""
        print("Worker started")

        workers = []

        for i in range(0, 5):
            worker = Worker(i)
            workers.append(worker)

        for worker in workers:
            worker.start()

        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            print("Stopping workers")
            for worker in workers:
                worker.stop()

        for worker in workers:
            worker.join()

    def __str__(self) -> str:
        return "Engine"


def start():
    """Start the worker"""
    start_http_server(8000)
    print("Metrics server started on port 8000")

    app = Engine()
    app.main()


if __name__ == "__main__":
    start()
