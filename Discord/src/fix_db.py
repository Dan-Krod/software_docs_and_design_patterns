import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '..', 'data', 'database.sqlite')

print(f"Спроба відкрити базу за шляхом: {os.path.abspath(db_path)}")

try:
    if not os.path.exists(db_path):
        print("Помилка: Файл бази даних не знайдено за вказаним шляхом!")
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash VARCHAR(200)")
        
        conn.commit()
        conn.close()
        print("✅ Колонку password_hash успішно додано!")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("ℹ️ Колонка вже існує, нічого додавати не потрібно.")
    else:
        print(f"❌ Помилка SQLite: {e}")
except Exception as e:
    print(f"❌ Сталася помилка: {e}")