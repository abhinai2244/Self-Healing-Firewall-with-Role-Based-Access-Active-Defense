import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SnortLogHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.last_position = 0

    def on_modified(self, event):
        if not event.is_directory:
            with open(event.src_path, 'r') as f:
                # Move to last known position
                f.seek(self.last_position)
                lines = f.readlines()
                self.last_position = f.tell()
                
                for line in lines:
                    if line.strip():
                        self.callback(line)

class SnortMonitor:
    def __init__(self, log_file, alert_callback):
        self.log_file = log_file
        self.alert_callback = alert_callback
        self.observer = Observer()

    def start(self):
        logging.info(f"Starting Snort Monitor on {self.log_file}")
        # Ensure file exists
        if not os.path.exists(self.log_file):
            open(self.log_file, 'a').close()

        event_handler = SnortLogHandler(self.alert_callback)
        # Watch the directory containing the file
        directory = os.path.dirname(os.path.abspath(self.log_file))
        self.observer.schedule(event_handler, path=directory, recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

import os
