import streamlit as st
from datetime import datetime, date
import database as db
import pandas as pd
import department

#function to verify doctor id
def verify_doctor_id(doctor_id):
    verify = False
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT id
            FROM doctor_record;
            """
        )
    for id in c.fetchall():
        if id[0] == doctor_id:
            verify = True
            break
    conn.close()
    return verify

#function to show doctor details given in a list
def show_doctor_details(list_of_doctors):
    doctor_titles = ["Doctor ID", "Name", "Age", "Gender", "Date of Birth (DD-MM-YYYY)",
                     "Blood group", "Department ID", "Department name", "Contact number",
                     "Alternate contact number", "SSN", "Email",
                     "Qualification", "Specialization", "Years of Experience", "Address",
                     "City", "State", "Zip code"]
    if len(list_of_doctors) == 0:
        st.warning("No data to show")
    elif len(list_of_doctors) == 1:
        doctor_details = [x for x in list_of_doctors[0]]
        doctor_series = pd.Series(data = doctor_details, index = doctor_titles)
        st.write(doctor_series)
    else:
        doctor_details = []
        for doctor in list_of_doctors:
            doctor_details.append([x for x in doctor])
        df = pd.DataFrame(data = doctor_details, columns = doctor_titles)
        st.write(df)

#function to calculate a doctor's age using their date of birth
def calculate_age(dob):
    today = date.today()
    age = today.year - dob.year - ((dob.month, dob.day) > (today.month, today.day))
    return age

#function to generate unique doctor id using current date and time
def generate_doctor_id():
    id_1 = datetime.now().strftime("%S%M%H")
    id_2 = datetime.now().strftime("%Y%m%d")[2:]
    id = f"DR-{id_1}-{id_2}"
    return id

#function to get the department name a doctor works in
def get_department_name(dept_id):
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT name
            FROM department_record
            WHERE id = :id;
            """,
            {"id": dept_id}
        )
    return c.fetchone()[0]

#create Doctor class that contains all the fields and methods to work in doctors' table in database
class Doctor:
    def __init__(self):
        self.name = str()
        self.id = str()
        self.age = int()
        self.gender = str()
        self.dob = str()
        self.blood_group = str()
        self.department_id = str()
        self.department_name = str()
        self.contact_number_1 = str()
        self.contact_number_2 = str()
        self.ssn = str()
        self.email = str()
        self.qualification = str()
        self.specialization = str()
        self.years_of_experience = int()
        self.address = str()
        self.city = str()
        self.state = str()
        self.zip_code = str()


    def add_doctor(self):
        st.write("Enter doctor details: ")
        self.name = st.text_input("Full name")
        gender = st.radio("Gender", ["Female", "Male", "Other"])
        if gender == "Other":
            gender = st.text_area("Please mention")
        self.gender = gender
        dob = st.date_input("Date of birth (YYYY/MM/DD)")
        st.info("If the required date is not in the calendar, please type in the box above.")
        self.dob = dob.strftime("%d-%m-%Y")
        self.age = calculate_age(dob)
        self.blood_group = st.text_area("Blood group")
        department_id = st.text_input("Department ID")
        if department_id == '':
            st.empty()
        elif not department.verify_department_id(department_id):
            st.error("Invalid Department ID")
        else:
            st.success("Verified")
            self.department_id = department_id
            self.department_name = get_department_name(department_id)
        self.contact_number_1 = st.text_input("Contact number")
        contact_number_2 = st.text_input("Alternative contact number (optional)")
        self.contact_number_2 = (lambda phone: None if phone == '' else phone)(contact_number_2)
        self.ssn = st.text_input('SSN')
        self.email = st.text_input("Email")
        self.qualification = st.text_input("Qualification")
        self.specialization = st.text_input("Specialization")
        self.years_of_experience = st.number_input('Years of experience', value = 0, min_value = 0, max_value = 100)
        self.address = st.text_input("Address")
        self.city = st.text_input("City")
        self.zip_code = st.text_input("Zipcode")
        self.id = generate_doctor_id()
        save = st.button("Save")

        if save:
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    INSERT INTO doctor_record (
                        id, name, age, gender, dob, blood_group,
                        department_id, department_name, contact_number_1,
                        contact_number_2, ssn, email,
                        qualification, specialization, years_of_experience,
                        address, city, state, zip_code
                    )
                    VALUES (
                        :id, :name, :age, :gender, :dob, :blood_group,
                        :dept_id, :dept_name, :phone_1, :phone_2, :uid, :email,
                        :qualification, :specialization, :address, :city, 
                        :state, :zip_code
                    )
                    """,
                    {"id": self.id, "name": self.name, "age": self.age, 
                     "gender": self.gender, "dob": self.dob, "blood_group": self.blood_group,
                     "dept_id": self.department_id, "dept_name": self.department_name, "phone_1": self.contact_number_1,
                     "phone_2": self.contact_number_2, "uid": self.ssn, "email": self.email,
                     "qualification": self.qualification, "specialization": self.specialization,
                     "experience": self.years_of_experience, "address": self.address, "city": self.city, "state": self.state,
                     "zipcode": self.zip_code}
                )
                st.success("Doctor details saved successfully.")
                st.write("Your Doctor ID is: ", self.id)
                conn.close()
    
    def update_doctor(self):
        id = st.text_input("Enter doctor ID of doctor to be updated")
        if id == '':
            st.empty()
        elif not verify_doctor_id(id):
            st.error("Invalid Doctor ID")
        else:
            st.success("Verified")
            conn, c = db.connection()

            with conn:
                c.execute(
                    """
                    SELECT * 
                    FROM doctor_id
                    WHERE id = :id;
                    """, 
                    {"id": id}
                )
                st.write("Here are the current details of the doctor: ")
                show_doctor_details(c.fetchall())
            st.write("Enter new doctor details: ")
            department_id = st.text_input("Department ID")
            if department_id == '':
                st.empty()
            elif not department.verify_department_id(department_id):
                st.error("Invalid Department ID")
            else:
                st.success("Verified")
                self.department_id = department_id
                self.department_name =  get_department_name(department_id)
            self.contact_number_1 = st.text_input("Contact number")
            contact_number_2 = st.text_input("Alternate contact number (optional)")
            self.contact_number_2 = (lambda phone: None if phone == '' else phone)(contact_number_2)
            self.email = st.text_input("Email")
            self.qualification = st.text_input("Qualification")
            self.specialization = st.text_input("Specialization")
            self.years_of_experience = st.number_input("Years of Experience", value = 0, min_value = 0, max_value =100)
            self.address = st.text_input("Address")
            self.city = st.text_input("City")
            self.zip_code = st.text_input("Zipcode")
            update = st.button("Update")

            if update:
                with conn:
                    c.execute(
                        """
                    SELECT dob
                    FROM doctor_record
                    WHERE id = :id;
                        """,
                        {"id": id}
                    )
                    dob = [int(d) for d in c.fetchone()[0].split("-")[::-1]]
                    dob = date(dob[0], dob[1], dob[2])
                    self.age = calculate_age(dob)
                with conn:
                    c.execute(
                        """
                        UPDATE doctor_record
                        SET age = :age, department_id = :dept_id,
                        department_name = :dept_name, contact_number_1 = :phone_1,
                        contact_number_2 = :phone_2, email = : email,
                        qualification = :qualification, specialization = :specialization,
                        years_of_experience = :years_of_experience, address = :address, city = :city,
                        state = :state, zipcode = :zip_code
                        """,
                        {
                           'id': id, 'age': self.age, 'dept_id': self.department_id,
                            'dept_name': self.department_name,
                            'phone_1': self.contact_number_1,
                            'phone_2': self.contact_number_2, 'email': self.email_id,
                            'qualification': self.qualification,
                            'specialization': self.specialization,
                            'experience': self.years_of_experience,
                            'address': self.address, 'city': self.city,
                            'state': self.state, 'zipcode': self.zip_code  
                        }
                    )
                st.success("Doctor details updated successfull.")
                conn.close()
    def delete_doctor(self):
        id = st.text_input("Enter Doctor ID of the doctor to be deleted")
        if id == '':
            st.empty()
        elif not verify_doctor_id(id):
            st.error("Invalid Doctor ID")
        else:
            st.success("Verified")
            conn, c = db.connection()

            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM doctor_record
                    WHERE id = :id;
                    """,
                    {"id", id}
                )
                st.write("Here are the details of the doctor to be deleted from database: ")
                show_doctor_details(c.fetchall())

                confirm = st.checkbox("Check this box to confirm deletion")
                if confirm:
                    delete = st.button("Delete")

                    if delete:
                        c.execute(
                            """
                            DELETE FROM doctor_record
                            WHERE id = :id  
                            """,
                            {"id": id}
                        )
                        st.success("Doctor details successfully deleted.")
            conn.close()
        
    def show_all_doctors(self):
        conn, c = db.connection()
        with conn:
            c.execute(
                """
                SELECT *
                FROM doctor_record;
                """
            )
            show_doctor_details(c.fetchall())
        conn.close()
    
    def search_doctors(self):
        id = st.text_input("Enter Doctor ID")
        if id == '':
            st.empty()
        elif not verify_doctor_id(id):
            st.error("Invalid Doctor ID")
        else:
            st.success("Verified")
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM doctor_record
                    WHERE id = :id;
                    """,
                    {"id": id}
                )
                st.write("Here are your doctor details: ")
                show_doctor_details(c.fetchall())
            conn.close()