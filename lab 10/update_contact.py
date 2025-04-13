import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="1234"  # твой пароль
)

cur = conn.cursor()

old_name = input("Введите имя контакта, который нужно изменить: ")

choice = input("Что вы хотите изменить? (1 - имя, 2 - номер): ")

if choice == "1":
    new_name = input("Введите новое имя: ")
    cur.execute("UPDATE PhoneBook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
elif choice == "2":
    new_phone = input("Введите новый номер телефона: ")
    cur.execute("UPDATE PhoneBook SET phone = %s WHERE first_name = %s", (new_phone, old_name))
else:
    print("Неверный выбор.")

conn.commit()
print("✅ Контакт обновлён!")

cur.close()
conn.close()
