import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="1234"  # замени, если у тебя другой пароль
)

cur = conn.cursor()

# Ввод данных с консоли
name = input("Enter name: ")
phone = input("Enter phone number: ")

# Вставка в таблицу
cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)", (name, phone))

conn.commit()
print("✅ Contact saved!")

cur.close()
conn.close()
