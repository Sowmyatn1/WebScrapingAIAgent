import sqlite3

def create_db():
    conn = sqlite3.connect('doctors.db')
    cursor = conn.cursor()

    # Create doctor table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctor (
        doctor_id INTEGER PRIMARY KEY,
        name TEXT,
        specialization TEXT,
        qualification TEXT,
        experience TEXT,
        consultation_fee REAL,
        location TEXT
        
    )
    ''')

    # Create availability table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS availability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER,
        date TEXT,
        available_slots TEXT,
        FOREIGN KEY (doctor_id) REFERENCES doctor (doctor_id)
    )
    ''')


    # Commit changes and close
    conn.commit()
    conn.close()
