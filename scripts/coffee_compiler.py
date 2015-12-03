import sys
import time
import logging
from subprocess import call

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CoffeeHandler(FileSystemEventHandler):

    def on_modified(self, event):
        path = event._src_path
        print path
        if path.endswith(".coffee"):
        	call(["coffee", "-c", path])

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(CoffeeHandler(), path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()