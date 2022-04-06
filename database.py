import sqlite3

con = sqlite3.connect("polyclinic.db")
cur = con.cursor()

sql = """\
CREATE TABLE IF NOT EXISTS doctor(
id INTEGER PRIMARY KEY,
doctor_name TEXT,
doctor_speciality TEXT,
appointment_cost INTEGER,
payroll_percentage INTEGER,
salary REAL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS patient(
id INTEGER PRIMARY KEY,
patient_name TEXT,
patient_dob INTEGER,
patient_address TEXT
);
CREATE TABLE IF NOT EXISTS receipt(
id INTEGER PRIMARY KEY,
reception_date TEXT,
patient_id INTEGER, 
doctor_id INTEGER,
FOREIGN KEY (patient_id) REFERENCES patient (id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (doctor_id) REFERENCES doctor (id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""


def create_db():
    cur.executescript(sql)
    cur.close()
    con.close()
