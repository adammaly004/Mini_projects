import random
import json
import ast
from cryptography.fernet import Fernet

PASSWORD = "123"
#publicKey, privateKey = rsa.newkeys(512)

key = Fernet.generate_key()

# Instance the Fernet class with the key

fernet = Fernet(b'Y6lCII0-1zXOBbKoukqeJX0s-Oq1vGn9N1Zfimd-ftQ=')


def encrypt(item):
    enc = fernet.encrypt(str(item).encode())
    enc = str(enc)
    enc = enc.replace("b'", '')
    enc = enc.replace("'", '')
    return enc


def decode(item):
    list = []
    for x in range(0, len(item)):
        byte = bytes(item[x], 'utf-8')
        dec = fernet.decrypt(byte).decode()
        dic = ast.literal_eval(dec)
        list.append(dic)

    return list


def save(name, password, email, username):
    table = ({
        name: {
            "password": password,
            "email": email,
            "username": username}
    })
    #table = rsa.encrypt(str(table).encode(),publicKey)
    enc = encrypt(table)
    with open("database.json", "r+") as f:
        database = json.load(f)
        database.append(enc)
        f.seek(0)
        json.dump(database, f, indent=4)


def find():
    print("Site name:")
    name = input()
    print("\n")
    with open("database.json", "r") as f:
        database = json.load(f)
        dec = decode(database)

        for x in range(0, len(dec)):
            try:
                print(dec[x][name]["password"])
                print(dec[x][name]["email"])
                print(dec[x][name]["username"])
                print("\n")
            except Exception:
                pass


def password():
    ALPHABET = ('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTYVWXYZ',
                '0123456789', '(,._-*~"<>/|!@#$%^&)+=')
    chars = []

    while len(chars) < 10:
        n = random.randint(0, len(ALPHABET)-1)
        alpha = ALPHABET[n]
        n = random.randint(0, len(alpha)-1)
        chars.append(alpha[n])

    return ''.join(chars)


def menu():
    print('-'*30)
    print(('-'*13) + 'Menu' + ('-' * 13))
    print('1. Create new password')
    print('2. Find all sites and apps connected to an email')
    print('3. Find a password for a site or app')
    print('Q. Exit')
    print('-'*30)
    return input('> ')


def create():
    while True:
        print("Enter the name of the application or page: ")
        name = input()
        print("Do you want to generate a password? yes/no")
        generate = input()
        if generate == "yes":
            passw = password()

        elif generate == "no":
            print('Enter your password: ')
            passw = input()
        else:
            break
        print("Enter your email: ")
        email = input()

        print("Enter your username: ")
        username = input()
        if username == None:
            username = ""

        save(name, passw, email, username)
        break


passw = input(
    'Enter password: ')

if passw == PASSWORD:
    print('You\'re in')

else:
    print('no luck')
    exit()

choice = menu()
while choice != 'Q':
    if choice == '1':
        create()
    if choice == '2':
        find()
    if choice == '3':
        print("find app")
    else:
        choice = menu()
exit()
