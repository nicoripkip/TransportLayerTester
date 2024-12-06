import threading
from dataclasses import dataclass


class MessageObject:
    def __init__(self, channel, data):
        self.channel = channel
        self.data = data

    def get_channel(self):
        return self.channel

    def get_data(self):
        return self.data


class MessageBuffer:
    _instance   = None
    _buffer     = []
    _lock       = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MessageBuffer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def publish(self, message):
        self._lock.acquire()
        self._buffer.append(message)
        self._lock.release()

    def subscribe(self, callback):
        self._lock.acquire()
        msg = self._buffer.pop(0)
        self._lock.release()

    def poll(self):
        pass


@dataclass
class MetaThread:
    thread_id: str
    thread: threading.Thread


class ThreadBuffer:
    _instance   = None
    _buffer     = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ThreadBuffer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def add_thread(self, thread_id, thread):
        self._buffer.append(MetaThread(thread_id, thread))

        print(self._buffer)

    def remove_thread(self, thread_id: str):
        for i in range(0, len(self._buffer)):
            if self._buffer[i].thread_id == thread_id:
                self._buffer.pop(i)
                return

        print("[error] Thread not found in list")