import sqlite3


def see_data(db_name="users.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS contacts;")
    d = conn.fetchall()
    conn.commit()
    conn.close()
    print(d)

# def drop_contacts_table(db_name="users.db"):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute("DROP TABLE IF EXISTS contacts;")
#     conn.commit()
#     conn.close()
#     print("contacts table dropped successfully.")

if __name__ == "__main__":
    see_data()
