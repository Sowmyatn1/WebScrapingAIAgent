import create_db
import sqlite3


conn = sqlite3.connect('doctors.db')
cursor = conn.cursor()

# Insert a doctor
cursor.execute('''
INSERT INTO doctor (doctor_id, name, specialization, location, consultation_fee, languages)
VALUES (?, ?, ?, ?, ?, ?)
''', (1270, "Dr B. L. Avinash", "General Practitioner", "Bangalore", 300, "English, Hindi, Telugu"))

# Insert a sample availability
cursor.execute('''
INSERT INTO availability (doctor_id, date, session, start_time, end_time, slot_url)
VALUES (?, ?, ?, ?, ?, ?)
''', (1270, "2025-10-14", "Morning", "11:00 AM", "11:25 AM",
      "https://web.medicasapp.com/cms/in/1270/general practitioner/11:00 AM/11:25 AM/2025-10-14"))

conn.commit()


conn = sqlite3.connect('doctors.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM doctor")
print(cursor.fetchall())

cursor.execute("SELECT * FROM availability")
print(cursor.fetchall())

conn.close()

