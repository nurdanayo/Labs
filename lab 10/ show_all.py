import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="1234"  # укажи свой пароль
)

cur = conn.cursor()

cur.execute("SELECT * FROM PhoneBook")
rows = cur.fetchall()

print("📋 PhoneBook contacts:")
for row in rows:
    print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

cur.close()
conn.close()
