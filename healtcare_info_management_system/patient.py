import streamlit as st
from datetime import datetime, date
import database as db
import pandas as pd

#function to verify patient id
def verify_patient_id(patient_id):
    verify = False
    conn, c = db.connection()
    with conn:
        c.execute(
            """"
            SELECT id
            FROM patient_record;
            """
        )
    for id in c.fetchall():
        if id[0] == patient_id:
            verify = True
            break
    conn.close()
    return verify


#function to generate unique patient id using current date and time
def generate_patient_id(reg_date, reg_time):
    id_1 = ''.join(reg_time.split(":")[::-1])
    id_2 = ''.join(reg_date.split('-')[::-1])[2:]
    id = f"P-{id_1}-{id_2}"
    return id

#function to calculate age using given date of birth
def calculate_age(dob):
    today = date.today()
    age = today.year - dob.year - ((dob.month, bod.year) > (today.month, today.day))
    return age 

#function to show patient details given in a list
def show_patient_details(list_of_patients):
    patient_titles = ["Patient ID", "Name", "Age", "Gender", "Date of birth (DD-MM-YYYY)", 
    "Blood group", "Contact number", "SSN", "Weight (kg)", "Height (cm)", "Address",
    "City", "State", "Zipcode", "Next of kin's name", "Next of kin's relation to patient",
    "Next of kin's contact number", "Email", "Date of registration (DD-MM-YYYY)", 
    "Time of registration (hh:mm:ss)"]
    if len(list_of_patients) == 0:
        st.warning("No data to show")
    elif len(list_of_patients) == 1:
        patient_details = [x for x in list_of_patients[0]]
        patient_series = pd.Series(data = patient_details, index = patient_titles)
        st.write(patient_series)
    else:
        patient_details = []
        for patient in list_of_patients:
            patient_details.append([x for x in patient])
        df = pd.DataFrame(data = patient_details, columns = patient_titles)
        st.write(df)

#patient class containing all the fields and methods required to work with patients' table in database
class Patient:
    def __init__(self):
        self.name = str()
        self.id = str()
        self.gender = str()
        self.age = int()
        self.contact_number = str()
        self.dob = str()
        self.blood_group = str()
        self.date_of_registration = str()
        self.time_of_registration = str()
        self.email = str()
        self.ssn = str()
        self.height = int()
        self.weight = int()
        self.next_of_kin_name = str()
        self.next_of_kin_relation_to_patient = str()
        self.next_of_kin_contact_number = str()
        self.address = str()
        self.city = str()
        self.state = str()
        self.zip_code = str()
    
    def add_patient(self):
        st.write("Enter patient details: ")
        self.name = st.text_input("Full name")
        self.gender = st.radio("Gender", ["Female", "Male", "Other"])
        if gender == "Other":
            gender = st.text_input("Please mention")
        self.gender = gender
        dob = st.date_input("Date of birth (YYYY/MM/DD)")
        st.info("If the required date is not in the calendar, please type it into the box above.")
        self.dob = dob.strftime("%d-%m-%Y")
        self.age = calculate_age(dob)
        self.blood_group = st.text_input("Blood group")
        self.contact_number = st.text_input("Contact number")
        self.ssn = st.text_input("SSN")
        self.weight = st.number_input("Weight in kg", value = 0, min_value = 0, max_value = 400)
        self.height = st.number_input("Height in cm", value = 0, min_value = 0, max_value = 275)
        self.address = st.text_area("Address")
        self.city = st.text_input("City")
        self.state = st.text_input("State")
        self.zip_code = st.text_input("Zipcode")
        self.next_of_kin_name = st.text_input("Next of kin's name")
        self.next_of_kin_relation_to_patient = st.text_input("Next of kin's relationship to patient")
        self.next_of_kin_contact_number = st.text_input("Next of kin's contact number")
        email = st.text_input("Email (optional)")
        self.email = (lambda email: None if email == '' else email)(email)
        self.date_of_registration = datetime.now().strftime("%d-%m-%Y")
        self.time_of_registration = datetime.now().strftime("%H:%M:%S")
        self.id = generate_patient_id(self.date_of_registration, self.time_of_registration)
        save = st.button("Save")

        if save:
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    INSERT INTO patient_record (
                        id, name, age, gender, dob, blood_group,
                        contact_number, ssn, weight, height, address,
                        city, state, zip_code, next_of_kin_name,
                        next_of_kin_relation_to_patient,
                        next_of_kin_contact_number, email,
                        date_of_registration, time_of_registration
                    )
                    VALUES (
                        :id, :name, :age, :gender, :dob, :blood_group,
                        :contact_number, :ssn, :weight, :height, :address,
                        :city, :state, :zip_code, :next_of_kin_name,
                        :next_of_kin_relation_to_patient, :next_of_kin_contact_number,
                        :email, :date_of_registration, :time_of_registration
                    );
                    """,
                    {
                        "id": id, "name": name, "age": age, "gender": gender,
                        "blood_group": blood_group, "contact_number": contact_number,
                        "ssn": ssn, "weight": weight, "height": height, "address": address,
                        "city": city, "state": state, "zip_code": zip_code, "next_of_kin_name": next_of_kin_name,
                        "next_of_kin_relation_to_patient": next_of_kin_relation_to_patient,
                        "next_of_kin_contact_number": next_of_kin_contact_number,
                        "email": email, "date_of_registration": date_of_registration, 
                        "time_of_registration": time_of_registration
                    }
                )
            st.success("Patient details saved successfully.")
            st.write("Your Patient ID is: ", self.id)
            conn.close()
    
    def update_patient(self):
        id = st.text_input("Enter Patient ID of patient to be updated")
        if id == '':
            st.empty()
        elif not verify_patient_id(id):
            st.error("Invalid Patient ID")
        else:
            st.success("Verified")
            conn, c = db.connection()
            
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM patient_record
                    WHERE id = :id;
                    """,
                    {"id": id}
                )
                st.write("Here are the patient's current details: ")
                show_patient_details(c.fetchall())
        st.write("Enter the patient's new details: ")
        self.contact_number = st.text_input("Contact number")
        self.weight = st.number_input("Weight in kg", value = 0, min_value = 0, max_value = 400)
        self.height = st.number_input("Height in cm", value = 0, min_value = 0, max_value = 275)
        self.address = st.text_area("Address")
        self.city = st.text_input("City")
        self.state = st.text_input("State")
        self.zip_code = st.text_input("Zipcode")
        self.next_of_kin_name = st.text_input("Next of kin's name")
        self.next_of_kin_relation_to_patient = st.text_input("Next of kin's relationship to patient")
        self.next_of_kin_contact_number = st.text_input("Next of kin's contact number")
        email = st.text_input("Email (optional)")
        self.email = (lambda email: None if email == '' else email)(email)
        self.date_of_registration = datetime.now().strftime("%d-%m-%Y")
        self.time_of_registration = datetime.now().strftime("%H:%M:%S")
        update = st.button("Update")

        if update:
            with conn:
                c.execute(
                    """ 
                    SELECT dob
                    FROM patient_record
                    WHERE id = :id;
                    """,
                    {"id": id}
                )
                
                dob = [int(d) for d in c.fetchone()[0].split('-'[::-1])]
                dob = date(dob[0], dob[1], dob[2])
                self.age = calculate_age(dob)
        with conn:
            c.execute(
                """ 
                UPDATE patient_record
                SET name = :name, age = :age, contact_number = :phone,
                weight = :weight, height = :height, address = :address,
                city = :city, state = :state, zip_code = :zip_code,
                next_of_kin_name = :kin_name, next_of_kin_relation_to_patient = :kin_relation,
                next_of_kin_contact_number = :kin_phone, email = :email, 
                date_of_registration = :date_of_registration, 
                time_of_registration = :time_of_registration
                WHERE id = :id;
                """,
                {
                    "id": id, "name": self.name, "age": self.age,
                    "phone": self.contact_number, "weight": self.weight,
                    "height": self.height, "address": self.address, "city": self.city,
                    "state": self.state, "zip_code": self.zip_code, 
                    "kin_name": self.next_of_kin_name, 
                    "kin_relation": self.next_of_kin_relation_to_patient,
                    "kin_phone": self.next_of_kin_contact_number, 
                    "date_of_registration": self.date_of_registration,
                    "time_of_registration": self.time_of_registration
                }
            )
        st.success("Patient details updated successfully.")
        conn.close()

    def delete_patient(self):
        id = st.text_input("Enter Patient ID of the patient to be removed")
        if id == '':
            st.empty()
        elif not verify_patient_id(id):
            st.error("Invalid Patient ID")
        else:
            st.success("Verified")
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM patient_id
                    WHERE id = :id;
                    """,
                    {"id": id}
                )
                st.write("Here are details about patient to be removed from database: ")
                show_patient_details(c.fetchall())

                confirm = st.checkbox("Check this box to confirm deletion")
                if confirm:
                    delete = st.button("Delete")

                    if delete:
                        c.execute(
                            """
                            DELETE FROM patient_record
                            WHERE id = :id;
                            """,
                            {"id": id}
                        )
                        st.success("Patient details removed successfully.")
            conn.close()
    
    def show_all_patients(self):
        conn, c = db.connection()
        with conn:
            c.execute(
                """
                SELECT *
                FROM patient_record;
                """
            )
            show_patient_details(c.fetchall())
        conn.close()
    
    def search_patients(self):
        id = st.text_input("Enter Patient ID...")
        if id == '':
            st.empty()
        elif not verify_patient_id(id):
            st.error("Invalid Patient ID")
        else:
            st.success("Verified")
            conn, c = db.connection()
            with conn: 
                c.execute(
                    """
                    SELECT *
                    FROM patient_record
                    WHERE id = :id;
                    """,
                    {"id": id}
                )
                st.write("Here are the patient's details")
                show_patient_details(c.fetchall())
                conn.close()
