import threading
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class MsgSubscriber:
    client_id: str
    callback: Callable


@dataclass
class MsgObject:
    topic: str
    data: List[str]
    subscribers: List[MsgSubscriber]


class MessageBuffer:
    _instance = None
    _lock = threading.Lock()


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print("Instance of buffer created")
                    cls._instance = super(MessageBuffer, cls).__new__(cls, *args, **kwargs)

                    # init other stuff in the class
                    cls._instance._buffer = {}

        return cls._instance


    def publish(self, topic: str, msg: str):
        self._lock.acquire()

        if topic not in self._buffer:
            self._buffer[topic] = MsgObject(topic, [], [])

        self._buffer[topic].data.append(msg)

        # print(self._buffer[topic].data)
        # print(self._buffer[topic].subscribers)

        self._lock.release()


    def subscribe(self, topic: str, client_id: str, callback: Callable):
        self._lock.acquire()

        if topic not in self._buffer:
            self._buffer[topic] = MsgObject(topic, [], [])

        self._buffer[topic].subscribers.append(MsgSubscriber(client_id, callback))

        self._lock.release()


    def size(self):
        return len(self._buffer)


    def poll(self):
        print(self._buffer)
        if  "tcpclient" in self._buffer:
            print(self._buffer["tcpclient"].data)

        for x in self._buffer.values():
            if len(x.data) > 0:
                print("Message in channel")
                msg = x.data.pop(0)
                for y in x.subscribers:
                    y.callback(msg)


    def check_lock(self):
        return self._lock.locked()


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