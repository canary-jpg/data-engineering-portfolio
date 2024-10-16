import sqlite3 as sql
import config

#establishing connection to database, enabling foreign key constraint support, and create cursor
def connection():
    conn = sql.connect(config.database_name + '.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    c = conn.cursor()
    return conn, c



#establishing connection to the database and create tables (if they don't exist yet)
def initialize_db():
    conn, c = connection()
    with conn:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS patient_record (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                contact_number_1 TEXT NOT NULL,
                contact_number_2 TEXT,
                uid TEXT NOT NULL UNIQUE,
                weight INTEGER NOT NULL,
                height INTEGER NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code INTEGER NOT NULL,
                next_of_kin_name TEXT NOT NULL,
                next_of_kin_relation_to_patient TEXT NOT NULL,
                next_of_kin_contact_number TEXT NOT NULL,
                email TEXT,
                date_of_registration TEXT NOT NULL,
                time_of_registration TEXT NOT NULL
            );
"""
        )
    with conn:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS doctor_record (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                dob TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                department_id INTEGER NOT NULL,
                department_name TEXT NOT NULL,
                contact_number TEXT NOT NULL,
                ssn TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                qualification TEXT NOT NULL,
                specialization TEXT NOT NULL,
                years_of_experience INTEGER NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code INTEGER NOT NULL,
                FOREIGN KEY (department_id) REFERENCES department_record(id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
            );
                """
        )
    with conn:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS prescription_record(
                id TEXT PRIMARY KEY,
                patient_id TEXT NOT NULL,
                patient_name TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                comments TEXT,
                medicine_1_name TEXT NOT NULL,
                medicine_1_dosage_desc TEXT NOT NULL,
                medicine_2_name TEXT,
                medicine_2_dosage_desc TEXT,
                medicine_3_name TEXT,
                medicine_3_dosage_desc TEXT,
                FOREIGN KEY (patient_id) REFERENCES patient_record(id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT,
                FOREIGN KEY (doctor_id) REFERENCES doctor_record(id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
            ); 
"""
        )
    with conn:
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS medical_test_record (
            id TEXT PRIMARY KEY,
            test_name TEXT NOT NULL,
            patient_id TEXT NOT NULL,
            patient_name TEXT NOT NULL,
            doctor_id TEXT NOT NULL,
            doctor_name TEXT NOT NULL,
            medical_lab_scientist_id TEXT NOT NULL,
            test_date_time TEXT NOT NULL,
            result_date_time TEXT NOT NULL,
            result_and_diagnosis TEXT,
            desc TEXT,
            comments TEXT,
            cost INTEGER NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patient_record(id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
            FOREIGN KEY (doctor_id) REFERENCES doctor_record(id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT

        );
"""
        )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    initialize_db()