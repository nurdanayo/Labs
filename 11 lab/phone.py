import psycopg2

# Connect to the database
conn = psycopg2.connect(
    dbname="phonebook_db",
    user="macbook",
    password="1234",  # Add your password if needed
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Insert or update a single user
def insert_one_user():
    name = input("Enter first name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone number (11 digits): ")
    cur.execute("CALL insert_or_update_user(%s, %s, %s)", (name, surname, phone))
    conn.commit()
    print("✅ User inserted or updated.\n")

# Insert multiple users with validation
def insert_many_users():
    print("Insert 3 users for demo:")
    user_list = [
        ['Aruzhan', 'Tursyn', '87001112233'],
        ['Fake', 'Invalid', 'abc123'],
        ['Aliya', 'Karimova', '87005556677']
    ]
    cur.execute("CALL insert_many_users(%s)", (user_list,))
    conn.commit()
    print("✅ Batch insert complete.\n")

# Search by pattern using function
def search_by_pattern():
    pattern = input("Search by name, surname, or phone: ")
    cur.execute("SELECT * FROM get_users_by_pattern(%s)", (pattern,))
    results = cur.fetchall()
    print("\n🔍 Search results:")
    for row in results:
        print(row)

# Paginate users
def show_paginated():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))
    cur.execute("SELECT * FROM get_paginated_users(%s, %s)", (limit, offset))
    print("\n📄 Paginated results:")
    for row in cur.fetchall():
        print(row)

# Delete user by name, surname, or phone
def delete_user():
    key = input("Enter name, surname, or phone to delete: ")
    cur.execute("CALL delete_user(%s)", (key,))
    conn.commit()
    print("🗑️ User deleted if found.\n")

# Menu
def main():
    while True:
        print("\n📱 PhoneBook Menu")
        print("1. Insert or update one user")
        print("2. Insert many users (test)")
        print("3. Search by pattern")
        print("4. Show paginated users")
        print("5. Delete user")
        print("6. Exit")
        choice = input("Choose option: ")

        if choice == "1":
            insert_one_user()
        elif choice == "2":
            insert_many_users()
        elif choice == "3":
            search_by_pattern()
        elif choice == "4":
            show_paginated()
        elif choice == "5":
            delete_user()
        elif choice == "6":
            break
        else:
            print("❌ Invalid option.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
