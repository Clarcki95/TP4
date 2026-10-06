from utils.list import List


class Queue:
    def __init__(self):
        self.list = List()

    def get_size(self):
        return self.list.size

    def is_empty(self):
        return self.list.size == 0

    def head(self):
        if self.is_empty():
            return None
        return self.list.get(0)

    def enqueue(self, value):
        self.list.add(value)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        value = self.head()
        self.list.remove(0)
        return value
