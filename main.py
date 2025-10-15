import sqlite3
from create_db import create_db
from insert_data import insert_data

def tables_exist(db_name="doctors.db", tables=("doctor", "availability")):
    """Check if all tables in 'tables' exist in the SQLite database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    existing_tables = []
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cursor.fetchall()
    existing_tables = [row[0] for row in rows]

    conn.close()
    
    # Return True if all required tables exist
    return all(table in existing_tables for table in tables)


if __name__ == "__main__":
    db_name = "doctors.db"
    
    # 1️⃣ Check if tables exist, create if they don't
    if not tables_exist(db_name):
        create_db()
    else:
        print("✅ Tables already exist, skipping creation.")

    # 2️⃣ Call your scraper and insert data
   # url = "https://medicasapp.com/in/doctors-in-bangalore/general-practitioner/dr-b-l-avinash/"
    url = "https://medicasapp.com/in/doctors-in-chennai/orthopedics/dr-hementha-kumar-govinda-rajan/"
    insert_data(url)
