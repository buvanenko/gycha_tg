import sqlite3

conn = sqlite3.connect('dialogs.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS dialogs (
    dialog_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

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



def add_message(dialog_id, role, content):
    try:
        # Проверяем, существует ли диалог. Если нет, создаем его.
        cursor.execute('INSERT OR IGNORE INTO dialogs (dialog_id) VALUES (?)', (dialog_id,))
        
        # Подсчитываем текущее количество сообщений для данного dialog_id
        cursor.execute('SELECT COUNT(*) FROM messages WHERE dialog_id = ?', (dialog_id,))
        count = cursor.fetchone()[0]
        
        # Если сообщений больше 15, удаляем самое старое
        if count >= 15:
            cursor.execute('''
            DELETE FROM messages
            WHERE message_id = (
                SELECT message_id FROM messages
                WHERE dialog_id = ?
                ORDER BY timestamp ASC
                LIMIT 1
            )
            ''', (dialog_id,))
        
        cursor.execute('''
        INSERT INTO messages (dialog_id, role, content)
        VALUES (?, ?, ?)
        ''', (dialog_id, role, content))
        
        conn.commit()
    
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении сообщения: {e}")

def get_messages_by_dialog_id(dialog_id):
    try:
        cursor.execute('''
        SELECT role, content, timestamp
        FROM messages
        WHERE dialog_id = ?
        ORDER BY timestamp ASC
        ''', (dialog_id,))
        
        rows = cursor.fetchall()
        
        messages = []
        for row in rows:
            role, content, timestamp = row
            messages.append({
                "role": role,
                "content": content
            })
        
        return messages
    
    except sqlite3.Error as e:
        print(f"Ошибка при получении сообщений: {e}")
        return []