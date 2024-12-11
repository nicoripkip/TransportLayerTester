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
        """
        Dundor method to make sure only 1 instance of the MessageBuffer class is created
        :param args:
        :param kwargs:
        :return: cls._instance
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print("Instance of buffer created")
                    cls._instance = super(MessageBuffer, cls).__new__(cls, *args, **kwargs)

                    # init other stuff in the class
                    cls._instance._buffer = {}

        return cls._instance


    def publish(self, topic: str, msg: str):
        """
        Method to publish data into the message buffer
        :param topic:
        :param msg:
        :return:
        """
        self._lock.acquire()

        if topic not in self._buffer:
            self._buffer[topic] = MsgObject(topic, [], [])

        self._buffer[topic].data.append(msg)

        # print(self._buffer[topic].data)
        # print(self._buffer[topic].subscribers)

        self._lock.release()


    def subscribe(self, topic: str, client_id: str, callback: Callable):
        """
        Method to register a client into the message buffer with a given callback
        :param topic:
        :param client_id:
        :param callback:
        :return:
        """
        self._lock.acquire()

        if topic not in self._buffer:
            self._buffer[topic] = MsgObject(topic, [], [])

        self._buffer[topic].subscribers.append(MsgSubscriber(client_id, callback))

        self._lock.release()


    def size(self):
        """
        Method to return the size of the message buffer
        :return: int
        """
        return len(self._buffer)


    def poll(self):
        """
        Method to poll the buffers and check if callback functions needs to be called
        :return:
        """
        # print(self._buffer)
        if  "tcpclient" in self._buffer:
            # print(self._buffer["tcpclient"].data)
            pass

        for x in self._buffer.values():
            if len(x.data) > 0:
                self._lock.acquire()

                # print("Message in channel")
                msg = x.data.pop(0)
                for y in x.subscribers:
                    y.callback(msg)

                self._lock.release()


@dataclass
class MetaThread:
    thread_id: str
    thread: threading.Thread


class ThreadBuffer:
    _instance   = None
    _buffer     = []
    _lock       = threading.Lock()


    def __new__(cls, *args, **kwargs):
        """
        Method to check if an instance is created
        :param args:
        :param kwargs:
        :return:
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ThreadBuffer, cls).__new__(cls, *args, **kwargs)

        return cls._instance


    def add_thread(self, thread_id, thread):
        """
        Method to push a thread into the buffer
        :param thread_id:
        :param thread:
        :return: None
        """
        self._lock.acquire()

        self._buffer.append(MetaThread(thread_id, thread))

        self._lock.release()


    def remove_thread(self, thread_id: str):
        """
        Method to pop a thread from the message buffer
        :param thread_id:
        :return: None
        """
        self._lock.acquire()

        for i in range(0, len(self._buffer)):
            if self._buffer[i].thread_id == thread_id:
                self._buffer.pop(i)

                self._lock.release()
                return

        self._lock.release()

        print("[error] Thread not found in list")