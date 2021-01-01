# Data Store

A file based key-value data store that supports create, read and delete (CRD) operations.

## Requirements 

Python 3 is required. Along with that, the following packages (built-in by default) are also required.
* [json](https://docs.python.org/3/library/json.html)
* [time](https://docs.python.org/3/library/time.html)

## Usage

```python
Store(path="./store.json")  
```
Initializes the store in the ```path```, if specified, otherwise in the default path ```./store.json```. Raises ```TypeError``` if the file is not of type ```JSON```.

```python
Store.create(key, value, ttl=None)
```
Creates a key-value pair, using the key of type ```str```, the value of type ```JSON``` and sets the ```ttl```, if specified, and saves it to the store. 

Raises ```KeyError``` if the ```key``` already exists or the length of the ```key``` exceeds 32 or the size of the ```value``` exceeds 16KB, ```TypeError``` if the ```key``` is not of type ```str``` or ```value``` is not of type ```dict``` or the ```ttl``` is not of type ```int```.

```python
Store.read(key)
```
If the key has not expired, returns the value of the ```key``` as a ```JSON``` object. If the ```key``` is not found or expired, ```KeyError``` is raised.

```python
Store.delete(key)
```
If the ```key``` has not expired, deletes the key-value pair from the store. If the ```key``` is not found or expired, ```KeyError``` is raised.


```python
Store.__loadStore(store)
```
A utility method that returns the ```JSON``` file in the ```store_path``` attribute as a Python Dictionary.

```python
Store.__persistStore()
```
A utility method that persists the current instance of ```store``` as a JSON file in ```store_path``` attribute.