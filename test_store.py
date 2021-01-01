from store import Store
import pytest
import json
import time

class TestForCreate:
    def test_one(self):
        store = Store("./test.json")
        key, value = "1", {"a": 1}
        assert store.create(key, value) == None
        store.delete(key)
    def test_two(self):
        store = Store("./test.json")
        key, value = "1", {"a": 1}
        store.create(key, value)
        with pytest.raises(KeyError):
            store.create(key, value)
        store.delete(key)
    def test_three(self):
        store = Store("./test.json")
        key, value = 1, {"a":1}
        with pytest.raises(TypeError):
            store.create(key, value)
    def test_four(self):
        store = Store("./test.json")
        key, value = "1", {"1"}
        with pytest.raises(TypeError):
            store.create(key, value)
    def test_five(self):
        store = Store("./test.json")
        key, value = "1", 1
        with pytest.raises(TypeError):
            store.create()
    def test_six(self):
        store = Store("./test.json")
        key, value = "1", "1"
        with pytest.raises(TypeError):
            store.create(key, value)
    def test_seven(self):
        store = Store("./test.json")
        key, value = "1", []
        with pytest.raises(TypeError):
            store.create(key, value)
    def test_eight(self):
        store = Store("./test.json")
        key, value = "a"*33, {"a":1}
        with pytest.raises(KeyError):
            store.create(key, value)
    def test_nine(self):
        store = Store("./test.json")
        key, value, ttl = "1", {"a": 1}, 10
        assert store.create(key, value, ttl) == None
        store.delete("1")

class TestForRead:
    def test_one(self):
        store = Store("./test.json")
        key, value = "k", {"a": 1}
        store.create(key, value)
        assert json.loads(store.read(key)) == value
        store.delete(key)
    def test_two(self):
        store = Store("./test.json")
        with pytest.raises(KeyError):
            json.loads(store.read("k"))
    def test_three(self):
        store = Store("./test.json")
        key, value, ttl = "k", {"a": 1}, 5
        store.create(key, value, ttl)
        time.sleep(ttl+1)
        with pytest.raises(KeyError):
            store.read(key)
    def test_four(self):
        store = Store("./test.json")
        key, value, ttl = "k", {"a": 1}, 5
        store.create(key, value, ttl)
        time.sleep(ttl-1)
        assert json.loads(store.read(key)) == value
        store.delete(key)

class TestForDelete:
    def test_one(self):
        store = Store("./test.json")
        key, value, ttl = "k", {"a": 1}, 5
        store.create(key, value, ttl)
        assert store.delete(key) == None
    def test_two(self):
        store = Store("./test.json")
        key, value, ttl = "k", {"a": 1}, 5
        store.create(key, value, ttl)
        time.sleep(ttl+1)
        with pytest.raises(KeyError):
            store.delete(key)
    def test_three(self):
        store = Store("./test.json")
        key, value, ttl = "k", {"a": 1}, 5
        store.create(key, value, ttl)
        time.sleep(ttl-1)
        assert store.delete(key) == None
    def test_four(self):
        store = Store("./test.json")
        with pytest.raises(KeyError):
            store.delete("k")