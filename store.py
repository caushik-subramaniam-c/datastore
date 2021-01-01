import json
from time import time

class Store:
    def __init__(self, path="./store.json"):
        self.__MAX_KEY_SIZE = 32
        self.__MAX_VALUE_SIZE = 16*1000
        self.__MAX_TIME = -1
        if not path.endswith('.json'):
            raise TypeError("File must be of type JSON")
        self.__store_path = path

    def __loadStore(self):
        try:
            with open(self.__store_path, "r") as data_store:
                store = json.load(data_store)
        except FileNotFoundError:
            with open(self.__store_path, "w") as data_store:
                store = {}
        except json.decoder.JSONDecodeError:
            store = {}
        return store

    def __persistStore(self, store):
        json.dump(store, open(self.__store_path, "w"), indent=4)

    def create(self, key, value, ttl=None):
        if ttl == None:
            ttl = self.__MAX_TIME
        if not isinstance(key, str):
            raise TypeError("Key must be of type string")
        if not isinstance(value, dict):
            raise TypeError("Value must be of type dict")
        if not isinstance(ttl, int):
            raise TypeError("TTL value must be an integer")
        if len(key) > self.__MAX_KEY_SIZE:
            raise KeyError("Key length must be less than %d"%self.__MAX_KEY_SIZE)
        if len(json.dumps(value).encode()) > self.__MAX_VALUE_SIZE:
            raise ValueError("Value must be less than %d"%self.__MAX_VALUE_SIZE)
        store = self.__loadStore()
        if key in store:
            raise KeyError("Key %s already exists"%key)
        store[key] = {"CREATED": int(time()),  "TTL": ttl, "VALUE": value}
        self.__persistStore(store)

    def read(self, key):
        store = self.__loadStore()
        expired_keys = []
        for k, v in store.items():
            if v["TTL"] != self.__MAX_TIME and int(time())-v["CREATED"]>v["TTL"]:
                expired_keys.append(k)
        for k in expired_keys:
            del store[k]
        self.__persistStore(store)
        if key in store:
            return json.dumps(store[key]["VALUE"])
        else:
            raise KeyError("Key %s doesn't exist"%key)

    def delete(self, key):
        store = self.__loadStore()
        expired_keys = []
        for k, v in store.items():
            if v["TTL"] != self.__MAX_TIME and int(time())-v["CREATED"]>v["TTL"]:
                expired_keys.append(k)
        for k in expired_keys:
            del store[k]
        if key not in store:
            self.__persistStore(store)
            raise KeyError("Key %s not found"%key)
        else:
            del store[key]
            self.__persistStore(store)
