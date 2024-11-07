from filelock import FileLock


class FileLocker:
    def __init__(self, path_to_lockfile: str):
        self.lock = FileLock(path_to_lockfile)

    def get_lock(self):
        return self.lock
