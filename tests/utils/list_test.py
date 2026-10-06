"""
Fichier: tests/utils/list_test.py
But: Test unitaire pour la classe List.
Auteur: Nino BELAOUD
"""
from utils.list import List

print("==============================")
print("utils/list.py")

list = List()

assert list.size == 0
assert list.first is None

list.add(42)

assert list.size == 1
assert list.first is not None
assert list.get(0) == 42
assert list.to_list() == [42]

list.add(43)

assert list.size == 2
assert list.first is not None
assert list.get(0) == 42
assert list.get(1) == 43
assert list.to_list() == [42, 43]

list.add(1, 0)

assert list.size == 3
assert list.first is not None
assert list.get(0) == 1
assert list.get(1) == 42
assert list.get(2) == 43
assert list.to_list() == [1, 42, 43]

list.add(2, 2)
assert list.size == 4
assert list.first is not None
assert list.get(0) == 1
assert list.get(1) == 42
assert list.get(2) == 2
assert list.get(3) == 43
assert list.to_list() == [1, 42, 2, 43]

list.add(50)

list.remove()

assert list.size == 4
assert list.first is not None
assert list.get(0) == 1
assert list.get(1) == 42
assert list.get(2) == 2
assert list.get(3) == 43
assert list.to_list() == [1, 42, 2, 43]

list.remove(1)
assert list.size == 3
assert list.first is not None
assert list.get(0) == 1
assert list.get(1) == 2
assert list.get(2) == 43
assert list.to_list() == [1, 2, 43]

list.remove(0)
assert list.size == 2
assert list.first is not None
assert list.get(0) == 2
assert list.get(1) == 43
assert list.to_list() == [2, 43]

list.remove()
assert list.size == 1
assert list.first is not None
assert list.get(0) == 2
assert list.to_list() == [2]

list.remove()
assert list.size == 0
assert list.first is None
assert list.to_list() == []

print("✅ Tests validés")
print("==============================")
