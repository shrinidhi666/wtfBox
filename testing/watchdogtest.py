#!/usr/bin/python
import sys
import time
# import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#LoggingEventHandler

class event_mine(FileSystemEventHandler):
    def on_any_event(self,event):
        print("wtf : "+ str(event))
        FileSystemEventHandler.on_any_event(self,event)




if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO,
                        # format='%(asctime)s - %(message)s',
                        # datefmt='%d-%m-%Y %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = event_mine()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()