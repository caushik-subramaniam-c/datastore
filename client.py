from store import Store
import json
import random
from getpass import getpass

class App:
    def __init__(self):
        self.store = Store()

    def signup(self, username, password, name):
        id = username
        try:
            self.store.create(id, {"name":name, "password": password})
            return 1
        except KeyError:
            return 0

    def login(self, username, password):
        try:
            user = json.loads(self.store.read(username))
            if user["password"] == password:
                return 1
        except KeyError:
            return 0

app = App()
print("Simple Auth App using data store")
case = input("\na. Sign up / b. Log in [a/B]? ")

if case == 'a':
    name = input("Name: ")
    username = input("Username: ")
    password = getpass("Password: ")

    if app.signup(username, password, name) == 1:
        print("Sign up success!")
    else:
        print("Sign up failed!")

elif case == 2 or case == "":
    username = input("Username: ")
    password = getpass("Password: ")
    if app.login(username, password) == 1:
        print("Log in success!")
    else:
        print("Log in failed!")