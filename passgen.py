from faker import Faker
import random
import requests
import string
from concurrent.futures import ThreadPoolExecutor

faker = Faker()
popular_replacements = {
    'A': '4',
    'A': '@',
    'S': '$',
    'B': '8',
    'E': '3',
    'G': '6',
    'I': '1',
    'L': '7',
    'O': '0',
    'S': '5',
    'T': '7',
    'Z': '2',
    'C': '9',
    'D': '0',
    'F': '7',
    'H': '4',
    'J': '9',
    'K': '4',
    'M': 'nn',
    'P': '9',
    'Y': '7'
}
rans = ["!", "*", "#", "$", "_", "%"]
words = requests.get('https://random-word-api.herokuapp.com/all').json()

def replace_letters(word):
    final = ''
    for letter in word:
        if letter.upper() in popular_replacements:
            if random.random() < 0.5:
                replaced_letter = popular_replacements[letter.upper()]
                final += replaced_letter
            else:
                final += letter
        else:
            if random.random() < 0.05:
                final += letter.upper()
            final += letter
    return final

def name():
    if random.random() < 0.5:
        name = faker.first_name()
    else:
        name = faker.last_name()
    if random.random() < 0.5:
        name = name.lower()
    return name

def date():
    date = str(faker.passport_dob()).split("-")[0]
    if random.random() < 0.6:
        date = date[2:]
    return date

def generate_password():
    word = name() if random.random() < 0.4 else ''.join(random.choice(string.ascii_lowercase) if random.random() < 0.95 else random.choice(string.ascii_uppercase) for _ in range(random.randint(3, 8)))
    special_char = random.choice(rans) if random.random() < 0.2 else ''
    random_num = ''.join(random.choice(string.digits) for _ in range(random.randint(1, 4)))
    d = date()
    w = random.choice(words)
    if random.random() < 0.45:
        word = replace_letters(word)
    if random.random() < 0.3:
        w = replace_letters(w)
    all = [word, special_char, d, w, random_num]
    for i in range(len(all)):
        if random.random() < 0.7:
            all[i] = ''
    random.shuffle(all)
    #selected_items = random.choices(list(set(all)), k=random.randint(2, 3))
    res = ''.join(all)
    if len(res) > 18 or len(res) <= 2 or isinstance(res, int):
        return generate_password()
    else:
        return res

def generate_passwords(amount):
    passwords = set()
    while len(passwords) < amount:
        password = generate_password()
        print(password)
        passwords.add(password)
    return passwords

amount = int(input('passwords: '))

with ThreadPoolExecutor() as executor:
    results = executor.submit(generate_passwords, amount).result()

open("passwords.txt", "x")
with open('passwords.txt', "a", encoding="utf-8") as file:
    for password in results:
        file.write(password + '\n')
