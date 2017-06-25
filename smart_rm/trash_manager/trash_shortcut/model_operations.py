import os
import shutil
from simple_rm.trash import Trash


def get_trash_by_model(trash_model):
    result_trash = Trash(
        trash_location=os.path.join(trash_model.location, trash_model.name),
        remove_mode=trash_model.remove_mode,
        dry_run=trash_model.dry_run
    )
    return result_trash


def get_trash_by_task(task_model):
    trash = get_trash_by_model(task_model.trash)
    trash.remove_mode = task_model.remove_mode
    trash.dry_run = task_model.dry_run
    return trash


def delete_trash_by_model(trash_model):
    trash_location = os.path.join(trash_model.location, trash_model.name)
    if os.path.exists(trash_location):
        shutil.rmtree(trash_location)
    trash_model.delete()
