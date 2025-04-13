import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="1234"  # ← твой пароль
)

cur = conn.cursor()

choice = input("Удалить по (1 - имени, 2 - номеру): ")

if choice == "1":
    name = input("Введите имя для удаления: ")
    cur.execute("DELETE FROM PhoneBook WHERE first_name = %s", (name,))
elif choice == "2":
    phone = input("Введите номер телефона для удаления: ")
    cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (phone,))
else:
    print("Неверный выбор.")

conn.commit()
print("✅ Контакт удалён (если найден).")

cur.close()
conn.close()
