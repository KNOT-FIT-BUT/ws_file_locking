
from time import sleep
import fcntl
import os

class FileLock():
    def __init__(self, file_path:str, mode="r+", timeout_sec=60):
        self.file_path = file_path
        self.mode = mode
        self.timeout_sec = timeout_sec
        
    def __enter__(self):
        f_locked_msg = False
        for _ in range(self.timeout_sec):
            try:
                self.file_lock = open(file=self.file_path, mode=self.mode)
                fcntl.flock(self.file_lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self.file_lock
            
            except IOError:
                if not f_locked_msg:
                    print("File locked, waiting...")
                    f_locked_msg = True     
                sleep(1)
                continue
        raise TimeoutError
        
    def __exit__(self, exc_type, exc_value, traceback):
        fcntl.flock(self.file_lock.fileno(), fcntl.LOCK_UN)
        self.file_lock.close()
        return True

