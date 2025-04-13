import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",  # или другая твоя игровая база
    user="postgres",
    password="1234"
)

cur = conn.cursor()

# Таблица пользователей
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
)
""")

# Таблица результатов
cur.execute("""
CREATE TABLE IF NOT EXISTS user_score (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    score INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    saved_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
print("✅ Таблицы users и user_score созданы!")

cur.close()
conn.close()
