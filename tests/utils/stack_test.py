from utils.stack import Stack

stack = Stack()

print("==============================")
print("utils/stack.py")

assert stack.is_empty()
assert stack.get_size() == 0
assert stack.head() is None

stack.push(1)

assert not stack.is_empty()
assert stack.get_size() == 1
assert stack.head() == 1

stack.pop()

assert stack.is_empty()
assert stack.get_size() == 0
assert stack.head() is None

stack.push(1)
stack.push(2)
stack.push(3)

assert not stack.is_empty()
assert stack.get_size() == 3
assert stack.head() == 3

stack.pop()

assert not stack.is_empty()
assert stack.get_size() == 2
assert stack.head() == 2

stack.pop()

assert not stack.is_empty()
assert stack.get_size() == 1
assert stack.head() == 1

stack.pop()

assert stack.is_empty()
assert stack.get_size() == 0
assert stack.head() is None

print("✅ Tests validés")
print("==============================")
