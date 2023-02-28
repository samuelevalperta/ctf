from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import random
import os
import signal
import string

TIMEOUT = 300

alph = string.ascii_letters + string.digits

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("CCIT{"))
assert(FLAG.endswith("}"))

db = {}

banner = """Welcome to Secure Password Generator!
Just choose your username, we create the password for you!"""

def generate_secure_random_password():
    with open("wordlist.txt", "r") as f:
        passwords = f.readlines()
    chosen = random.choice(passwords).strip() # removing trailing \n
    cipher = DES.new(key = b"\x00"*8, mode = DES.MODE_ECB)
    random_psw = cipher.encrypt(pad(chosen.encode(), 8))
    return random_psw.hex()[:12]

def register_admin():
    db["admin"] = generate_secure_random_password()

def register():
    user = input("Enter your username: ")
    if not all(x in alph for x in user):
        print("Invalid username!")
        return
    if user in db:
        print("Unfortunately this username is already taken!")
        return
    psw = generate_secure_random_password()
    db[user] = psw
    print(f"Here is your super secure password: {psw}")
    print("Be sure to keep it safe!")

def login():
    user = input("Enter your username: ")
    if user not in db:
        print("Username not found!")
        return
    psw = input("Enter your password: ")
    if psw == db[user]:
        print(f"Welcome back {user}!")
        if user == "admin":
            print(f"Here is your flag: {FLAG}")
        else:
            print("Unfortunately there is nothing for you here...")
    else:
        print("Looks like your password is wrong!")

def handle():
    register_admin() # Let's create a secure account for our admin!
    print(banner)

    while True:
        print("What do you want to do?")
        print("1. Register")
        print("2. Login")
        print("0. Exit")
        ch = int(input("> "))
        if ch == 1:
            register()
        elif ch == 2:
            login()
        else:
            break

if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
