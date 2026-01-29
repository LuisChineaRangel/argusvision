import sys
import subprocess
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os

class RestartOnChange(FileSystemEventHandler):
    def __init__(self, cmd, env=None):
        self.cmd = cmd
        self.env = env
        self.proc = subprocess.Popen(cmd, env=env)

    def on_modified(self, event):
        if Path(str(event.src_path)).suffix == ".py":
            print(f"\nDetected change in {event.src_path}. Restarting...")
            self.proc.kill()
            self.proc = subprocess.Popen(self.cmd, env=self.env)

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    src_path = project_root / "src"

    env = os.environ.copy()
    env["PYTHONPATH"] = str(src_path) + os.pathsep + env.get("PYTHONPATH", "")

    handler = RestartOnChange([sys.executable, "-m", "argusvision.main"], env=env)
    observer = Observer()
    observer.schedule(handler, str(project_root), recursive=True)
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
