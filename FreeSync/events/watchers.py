import time
import sys
from watchdog.observers import Observer
from .handlers import Handler

class Watcher():
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, '/Users/erincihatsaricilar/Documents/General', recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

