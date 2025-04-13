import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="1234"  # <-- замени на тот пароль, который ты установила при сбросе
)

cur = conn.cursor()

# Создание таблицы PhoneBook
cur.execute("""
CREATE TABLE IF NOT EXISTS PhoneBook (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    phone VARCHAR(20)
)
""")

conn.commit()
print("Таблица создана!")

cur.close()
conn.close()
