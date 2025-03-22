import sqlite3
import json

# Подключение к базе данных (или создание, если её нет)
conn = sqlite3.connect('dialogs.db')
cursor = conn.cursor()

# Создание таблицы для диалогов
cursor.execute('''
CREATE TABLE IF NOT EXISTS dialogs (
    dialog_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Создание таблицы для сообщений
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dialog_id TEXT,
    role TEXT,
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dialog_id) REFERENCES dialogs(dialog_id)
)
''')

conn.commit()

def migrate_json_to_sqlite(json_data):
    for dialog_id, messages in json_data.items():
        print(f"Processing dialog_id: {dialog_id}")
        # Добавляем диалог в таблицу dialogs
        cursor.execute('INSERT OR IGNORE INTO dialogs (dialog_id) VALUES (?)', (dialog_id,))
        
        # Добавляем каждое сообщение в таблицу messages
        for message in messages:
            print(f"Processing message: {message}")
            role = message["role"]
            content = message["content"]

            cursor.execute('''
            INSERT INTO messages (dialog_id, role, content)
            VALUES (?, ?, ?)
            ''', (dialog_id, role, content))
    
    conn.commit()

with open('dialogs.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)
# Пример использования
migrate_json_to_sqlite(json_data)