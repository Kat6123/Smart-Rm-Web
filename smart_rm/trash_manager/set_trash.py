import os
import shutil
import multiprocessing
import time
from simple_rm.trash import Trash


MAX_ITEMS_PER_TASK = 10000


def get_trash_by_model(trash_model):
    result_trash = Trash(
        trash_location=os.path.join(trash_model.location, trash_model.name),
        remove_mode=trash_model.remove_mode,
        dry_run=trash_model.dry_run
    )

    return result_trash


def delete_trash_by_model(trash_model):
    trash_location = os.path.join(trash_model.location, trash_model.name)
    if os.path.exists(trash_location):
        shutil.rmtree(trash_location)
    trash_model.delete()


def restore_by_trash_model(trash_model, paths_to_restore):
    trash = get_trash_by_model(trash_model)
    res = ((os.path.basename(path) for path in paths_to_restore))
    for i in res:
        print i
    return res


class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            print '%s: %s' % (proc_name, next_task)
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

    def __str__(self):
        return 'Hello'


def parallel_remove(trash, paths_to_remove):
    num_jobs = 0

    lock_trash = multiprocessing.Manager().Lock()
    lock_remove = multiprocessing.Manager().Lock()

    result = []
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
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

    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    finish = time.time()
    working_time = finish - start

    # Start printing results
    while num_jobs:
        result.extend(results.get())
        num_jobs -= 1

    print working_time

    return result
