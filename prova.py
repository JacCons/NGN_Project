from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class SimpleHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print ("Hello")
        print(event.src_path)
        if event.src_path == '/Users/jacopo/Desktop/NGN_Project/server1.txt':
            print(f"File {event.src_path} è stato modificato!")

if __name__ == "__main__":
    path = "."  # Directory da monitorare
    event_handler = SimpleHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
