import os
from simple_rm.trash import Trash as Trash_api
from trash_manager.models import Trash


def get_trash_by_model(trash_model):
    result_trash = Trash_api(
        trash_location=os.path.join(trash_model.location, trash_model.name),
        remove_mode=trash_model.remove_mode,
        dry_run=trash_model.dry_run
    )

    return result_trash
