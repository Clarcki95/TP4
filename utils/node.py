class Node:
    def __init__(self, value):
        self.value = value
        self.next: Node | None = None

    def set_next(self, next):
        self.next = next
