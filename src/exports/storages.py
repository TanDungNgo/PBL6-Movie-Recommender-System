from django.core.files.storage import default_storage


def save(fpath, file_obj, overwrite=False):
    if overwrite:
        default_storage.delete(fpath)
    return default_storage.save(fpath, file_obj)