from utils.queue import Queue

print("==============================")
print("utils/queue.py")

queue = Queue()

assert queue.is_empty()
assert queue.get_size() == 0

queue.enqueue(1)

assert not queue.is_empty()
assert queue.get_size() == 1
assert queue.head() == 1

queue.enqueue(2)

assert not queue.is_empty()
assert queue.get_size() == 2
assert queue.head() == 1

assert queue.dequeue() == 1
assert not queue.is_empty()
assert queue.get_size() == 1
assert queue.head() == 2

assert queue.dequeue() == 2
assert queue.is_empty()
assert queue.get_size() == 0
assert queue.head() is None

print("✅ Tests validés")
print("==============================")
