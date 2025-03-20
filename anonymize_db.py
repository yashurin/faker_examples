from faker import Faker
import sqlite3

fake = Faker('en_US')


def create_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Create 'users' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL,
        address TEXT NOT NULL
    )
    """)

    conn.commit()
    return conn


def populate_db(conn, num_records=10):
    fake = Faker()
    cursor = conn.cursor()

    for _ in range(num_records):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        address = fake.address()

        cursor.execute("""
        INSERT INTO users (name, email, phone, address)
        VALUES (?, ?, ?, ?)
        """, (name, email, phone, address))

    conn.commit()


def anonymize_database(db_name="users.db"):
    """Anonymize the SQLite database by replacing the 'real' data by fakes"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, phone, address FROM users")
    users = cursor.fetchall()

    for user in users:
        user_id, _, _, _, _ = user
        new_name = fake.name()
        new_email = fake.email()
        new_phone = fake.phone_number()
        new_address = fake.address()

        cursor.execute("""
            UPDATE users
            SET name = ?, email = ?, phone = ?, address = ?
            WHERE id = ?
        """, (new_name, new_email, new_phone, new_address, user_id))

    conn.commit()
    conn.close()


def main():
    conn = create_db()
    populate_db(conn)

    # Verify the insertion
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

    anonymize_database()

    # Verify anonymization
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()


if __name__ == "__main__":
    main()
