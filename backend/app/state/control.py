# app/state/control.py

import threading

class IngestControl:
    def __init__(self):
        self._lock = threading.Lock()
        self._enabled = True

    def is_enabled(self):
        with self._lock:
            return self._enabled

    def toggle(self, value: bool):
        with self._lock:
            self._enabled = value

ingest_control = IngestControl()