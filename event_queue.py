import Queue

class EventQueue(object):
    """Provides event queuing.

    @ivar q: event queuing object.
    """

    def __init__(self):
        self.q = Queue.Queue()

    def push(self, event_name=None, data=None):
        self.q.put({
            'name': event_name,
            'data': data
        })

    def get(self):
        return self.q.get()

    def empty(self):
        return self.q.empty()

    def join_thread(self):
        return self.q.join_thread()

    def close(self):
        return self.q.close()
