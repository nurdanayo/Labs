import psycopg2
import csv
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

def connect():
    return psycopg2.connect(
        host="localhost",
        database="phonebook_db",
        user="postgres",
        password="1234"  # ← замени на свой пароль
    )

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)", (name, phone))
    print(Fore.GREEN + "✅ Contact added!")

def insert_from_csv():
    file = input("Enter CSV file name (e.g. contacts.csv): ")
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                with open(file, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)", (row[0], row[1]))
        print(Fore.GREEN + "✅ Contacts added from CSV!")
    except FileNotFoundError:
        print(Fore.RED + f"❌ File '{file}' not found.")

def show_all():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM PhoneBook")
            rows = cur.fetchall()
            print(Fore.CYAN + "\n📋 All Contacts:")
            for row in rows:
                print(f"{Fore.WHITE}ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

def update_contact():
    name = input("Enter name of contact to update: ")
    choice = input("What to update? (1 - name, 2 - phone): ")
    with connect() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                new_name = input("Enter new name: ")
                cur.execute("UPDATE PhoneBook SET first_name = %s WHERE first_name = %s", (new_name, name))
                print(Fore.GREEN + "✅ Name updated!")
            elif choice == "2":
                new_phone = input("Enter new phone: ")
                cur.execute("UPDATE PhoneBook SET phone = %s WHERE first_name = %s", (new_phone, name))
                print(Fore.GREEN + "✅ Phone updated!")
            else:
                print(Fore.RED + "❌ Invalid choice.")

def delete_contact():
    choice = input("Delete by (1 - name, 2 - phone): ")
    with connect() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                name = input("Enter name: ")
                cur.execute("DELETE FROM PhoneBook WHERE first_name = %s", (name,))
            elif choice == "2":
                phone = input("Enter phone: ")
                cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (phone,))
            else:
                print(Fore.RED + "❌ Invalid choice.")
                return
    print(Fore.GREEN + "✅ Contact deleted (if found).")

def export_to_csv():
    file = input("Enter file name to save (e.g. export.csv): ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT first_name, phone FROM PhoneBook")
            rows = cur.fetchall()
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["first_name", "phone"])
                writer.writerows(rows)
    print(Fore.MAGENTA + f"📤 Contacts exported to '{file}'!")

def main():
    while True:
        print(Fore.BLUE + "\n📱 PhoneBook Menu")
        print("1 - Add contact (console)")
        print("2 - Add contacts from CSV")
        print("3 - Show all contacts")
        print("4 - Update contact")
        print("5 - Delete contact")
        print("6 - Export contacts to CSV")
        print("0 - Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            show_all()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            export_to_csv()
        elif choice == "0":
            print(Fore.YELLOW + "👋 Goodbye!")
            break
        else:
            print(Fore.RED + "❌ Invalid option.")

if __name__ == "__main__":
    main()




