import os
import shutil


class Filesystem:

    def __init__(self, path: str):
        self.path = path

    def clean(self):
        try:
            shutil.rmtree(self.path)
        except OSError:
            pass

    def init_directories(self):
        try:
            os.makedirs(self.path)
            os.makedirs(os.path.join(self.path, "users"))
        except OSError:
            pass
