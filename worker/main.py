#!/usr/bin/env python3

import random
import threading
from time import sleep

from prometheus_client import Counter, Gauge, Histogram, start_http_server

WORKER_CREATED = Counter("worker_created_total", "Number of workers created")
WORKER_STARTED = Counter("worker_started_total", "Number of workers started")
WORKER_STOPPED = Counter("worker_stopped_total", "Number of workers stopped")
ACTIVE_WORKERS = Gauge("workers_active", "Number of active workers")
WORK_DURATION = Histogram(
    "worker_operation_duration_seconds", "Time spent on each work operation"
)


class Worker(threading.Thread):
    def __init__(self, worker_id):
        super().__init__()
        print(f"Worker created {worker_id}")
        self.stopped = False
        self.name = worker_id
        WORKER_CREATED.inc()
        ACTIVE_WORKERS.inc()

    def run(self):
        print("Worker running")
        WORKER_STARTED.inc()

        while not self.stopped:
            print(f"Worker working {self.name}")
            with WORK_DURATION.time():
                sleep(random.randint(1, 5))

    def stop(self):
        print(f"Worker stopped {self.name}")
        self.stopped = True
        WORKER_STOPPED.inc()
        ACTIVE_WORKERS.dec()


class Engine:
    def main(self):
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


def start():
    start_http_server(8000)
    print("Metrics server started on port 8000")

    app = Engine()
    app.main()


if __name__ == "__main__":
    start()
