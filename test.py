
import json


def load():
    global context
    try:
        with open('dialogs.json', 'r', encoding='utf-8') as f:
            context = json.load(f)
    except FileNotFoundError:
        print('Немаэ')

def save():
    with open('dialogs.json', 'w', encoding='utf-8') as f:
        json.dump(context, f)

load()
print(context)