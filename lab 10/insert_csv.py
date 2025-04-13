import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="1234"  # ← замени на твой пароль
)

cur = conn.cursor()

with open('contacts.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Пропускаем заголовок
    for row in reader:
        cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)", (row[0], row[1]))

conn.commit()
print("📥 Контакты из CSV успешно добавлены!")

cur.close()
conn.close()
