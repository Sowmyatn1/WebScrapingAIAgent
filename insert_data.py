import sqlite3
from webscrape_doc import get_web_data  # import your scraping function

def insert_data(url):
    doctor_dict, available_dates_dict = get_web_data(url)

    conn = sqlite3.connect("doctors.db")
    cursor = conn.cursor()

    # Insert doctor details
    cursor.execute("""
        INSERT INTO doctor (doctor_id,name, specialization, qualification, experience, consultation_fee, location)
        VALUES (?,?, ?, ?, ?, ?, ?)
    """, (
        doctor_dict.get("doctor_id"),
        doctor_dict.get("name"),
        doctor_dict.get("specialization"),
        doctor_dict.get("qualification"),
        doctor_dict.get("experience"),
        doctor_dict.get("consultation_fee"),
        doctor_dict.get("location")
    ))

    
    # Insert availability details
    for date, slots in available_dates_dict.items():
        slots_str = ", ".join(slots) if isinstance(slots, list) else str(slots)
        cursor.execute("""
            INSERT INTO availability (doctor_id, date, available_slots)
            VALUES (?, ?, ?)
        """, (
            doctor_dict.get("doctor_id"),
            date,
            slots_str
        ))

    conn.commit()
    conn.close()
    print(f"✅ Data for {doctor_dict.get('name')} saved successfully!")

