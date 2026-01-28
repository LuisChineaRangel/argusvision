import sys
import subprocess
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartOnChange(FileSystemEventHandler):
    def __init__(self, cmd):
        self.cmd = cmd
        self.proc = subprocess.Popen(cmd)

    def on_modified(self, event):
        if Path(str(event.src_path)).suffix == ".py":
            print(f"\nDetected change in {event.src_path}. Restarting...")
            self.proc.kill()
            self.proc = subprocess.Popen(self.cmd)

if __name__ == "__main__":
    handler = RestartOnChange([sys.executable, "argusvision.py"])
    observer = Observer()
    observer.schedule(handler, ".", recursive=True)
    observer.start()

    print("Watcher active. Monitoring for changes... Press Ctrl+C or Esc to stop.")

    try:
        while True:
            if handler.proc.poll() is not None:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
    finally:
        observer.stop()
        if handler.proc.poll() is None:
            handler.proc.kill()

    observer.join()
