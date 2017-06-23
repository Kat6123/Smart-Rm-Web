import multiprocessing
import time


MAX_ITEMS_PER_TASK = 10000


class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            next_task = self.task_queue.get()

            if next_task is None:
                self.task_queue.task_done()
                break

            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task(object):
    def __init__(self, trash, items_to_remove, lock_trash, lock_remove):
        self.trash = trash
        self.items = items_to_remove
        self.lock_trash = lock_trash
        self.lock_remove = lock_remove

    def __call__(self):
        return self.trash.synchronized_remove(
            self.items, self.lock_trash, self.lock_remove
        )


def parallel_remove(trash, paths_to_remove):
    num_jobs = 0

    lock_trash = multiprocessing.Manager().Lock()
    lock_remove = multiprocessing.Manager().Lock()

    result = []

    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    num_consumers = multiprocessing.cpu_count() * 2
    consumers = [Consumer(tasks, results) for i in xrange(num_consumers)]

    for w in consumers:
        w.start()

    start = time.time()

    for start_pos in xrange(0, len(paths_to_remove), MAX_ITEMS_PER_TASK):
        tasks.put(
            Task(
                trash,
                paths_to_remove[start_pos:start_pos + MAX_ITEMS_PER_TASK],
                lock_trash, lock_remove)
            )
        num_jobs += 1

    for i in xrange(num_consumers):
        tasks.put(None)

    tasks.join()

    finish = time.time()
    working_time = finish - start

    while num_jobs:
        result.extend(results.get())
        num_jobs -= 1

    return result, working_time


def remove(trash, paths):
    start = time.time()
    result = trash.remove(paths)
    finish = time.time()

    return result, finish - start
