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


def delete_trash_by_model(trash_model):
    trash_location = os.path.join(trash_model.location, trash_model.name)
    if os.path.exists(trash_location):
        shutil.rmtree(trash_location)
    trash_model.delete()


def restore_by_trash_model(trash_model, paths_to_restore):
    trash = get_trash_by_model(trash_model)
    res = ((os.path.basename(path) for path in paths_to_restore))
    return trash.restore(res)


def clean_by_trash_model(trash_model, paths_to_remove):
    trash = get_trash_by_model(trash_model)
    return trash.remove_files_from_trash_permanently(paths_to_remove)
