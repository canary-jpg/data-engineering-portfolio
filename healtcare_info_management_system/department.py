import streamlit as st
from datetime import datetime
import database as db
import pandas as pd


#function that verifies department id
def verify_department_id(department_id):
    verify = False
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT id
            FROM department_record;
            """
        )
        for id in c.fetchall():
            if id[0] == department_id:
                verify = True
                break
            conn.close()
            return verify
        


#function to show the details of department(s) give in a list 
def show_department_details(list_of_departments):
    department_titles = ["Department ID", "Department name", "Description", "Contact number",
                         "Alternate contact number", "Address", "Email ID"]
    if len(list_of_departments) == 0:
        st.warnings("No data to show")
    elif len(list_of_departments) == 1:
        department_details = [x for x in list_of_departments[0]]
        dept_series = pd.Series(data = department_details, index = department_titles)
        st.write(dept_series)
    else:
        department_details = []
        for department in list_of_departments:
            department_details.append([x for x in department])
        df = pd.DataFrame(data = department_details, columns = department_titles)
        st.write(df)


#function to generate unique department id using current date and time
def generate_department_id():
    id_1 = datetime.now().strftime("%S%M%H")
    id_2 = datetime.now().strftime("%Y%m%d")[2:]
    id = f'D-{id_1}-{id_2}'
    return id 

#function to show the doctor id and name of doctor(s) given in a list 
def show_list_of_doctors(list_of_doctors):
    doctor_titles = ['Doctor ID', 'Name']
    if len(list_of_doctors) == 0:
        st.warning("No data to show")
    else:
        doctor_details = []
        for doctor in list_of_doctors:
            doctor_details.append([x for x in doctor])
        df = pd.DataFrame(data = doctor_details, columns = doctor_titles)
        st.write(df)

#function to fetch department name from database for the given department id
def get_department_name(dept_id):
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT name
            FROM department_record
            WHERE id = :id;
            """,
            {"id", dept_id}
        )
    return c.fetchone()[0]

#class containing all the fields and methods required to work the departments' table in the database

class Department:
    def __init__(self):
        self.name = str()
        self.id = str()
        self.description = str()
        self.contact_number_1 = str()
        self.contact_number_2 = str()
        self.address = str()
        self.email = str()
    
    def add_department(self):
        st.write('Enter department details: ')
        self.name = st.text_input('Department name')
        self.description = st.text_input("Description")
        self.contact_number_1 = st.text_input("Contact number")
        contact_number_2 = st.text_input("Alternative contact number (optional)")
        self.contact_number_2 = (lambda phone: None if phone == '' else phone)(contact_number_2)
        self.address = st.text_area("Address")
        self.email = st.text_input('Email')
        self.id = generate_department_id()
        save = st.button('Save')

        if save:
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    INSERT INTO department_record (
                        id, name, desc, contact_number_1, contact_number_2, address, email
                    )
                    VALUES (
                        :id, :name, :desc, :phone_1, :phone_2, :address, :email
                    );
                    """,
                    {"id": self.id, "name": self.name, "desc": self.description, "phone_1": self.contact_number_1,
                     "phone_2": self.contact_number_2, "address": self.address, "email": self.email}
                )
        st.success("Department details saved successfully")
        st.write("The Department ID is: ", self.id)
        conn.close()
    def update_department(self):
        id = st.text_input("Enter Department ID of the department to be updated")
        if id == '':
            st.empty()
        elif not verify_department_id(id):
            st.error("Invalid Department ID")
        else:
            st.success("Verified")
            conn, c = db.connection()

            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM department_record
                    WHERE id = :id;
                    """,
                    {"id": id}
                )
                st.write("Here are the current details of the department: ")
                show_department_details(c.fetchall())
        st.write("Enter new details of the department")
        self.desc = st.text_area("Description")
        self.contact_number_1 = st.text_input('Contact number')
        contact_number_2 = st.text_input("Alternative contact number (optional)")
        self.contact_number_2 = (lambda phone: None if phone == '' else phone)(contact_number_2)
        self.address = st.text_area("Address")
        self.email = st.text_area("Email")
        update = st.button("Update")

        if update:
            with conn:
                c.execute(
                    """
                    UPDATE department_record
                    SET desc = :desc,
                    contact_number_1 = :phone_1, contact_number_2 = :phone_2,
                    address = :address, email = :email
                    WHERE id = :id;
                    """,
                {"id": id, "desc": self.description, "phone_1": self.contact_number_1,
                 "phone_2": self.contact_number_2, "address": self.address,
                 "email": self.email}
                )
        st.success("Department details updated successfully.")
        conn.close(2)
    def delete_department(self):
        id = st.text_area("Enter Department ID of the deparment to be deleted")
        if id == '':
            st.empty()
        elif not verify_department_id(id):
            st.error('Invalid Department ID')
        else:
            st.success('Verified')
            conn, c = db.connection()

            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM department_record
                    WHERE id = :id
                    """,
                    {id: id}   
                )
                st.write("Here are the details of the department to be deleted: ")
                show_department_details(c.fetchall())

                confirm = st.checkbox("Check this box to confirm deletion")
                if confirm:
                    delete = st.button("Delete")

                    if delete:
                        c.execute(
                            """
                            DELETE FROM department_record
                            WHERE id = :id
                            """, 
                            {"id": id}
                        )
                        st.success("Department details deleted successfully.")
            conn.close()

    def search_department(self):
        id = st.text_area("Enter Department ID")
        if id == '':
            st.empty()
        elif not verify_department_id(id):
            st.error('Invalid Department ID')
        else:
            st.success('Verified')
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM department_record
                    WHERE id = :id;
                    """,
                    {"id": id}
                )
                st.write("Here are the details of the department: ")
                show_department_details(c.fetchall())
            conn.close()
    def list_dept_doctors(self):
        dept_id = st.text_area("Enter Department ID to find doctors in that department")
        if dept_id == '':
            st.empty()
        elif not verify_department_id(dept_id):
            st.error('Invalid Department ID')
        else:
            st.success("Verified")
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT id, name
                    FROM department_record
                    WHERE department_id = :dept_id;
                    """,
                    {"dept_id": dept_id}
                )
                st.write("Here is the list of doctors working in the ", get_department_name(dept_id), " department: ")
                show_list_of_doctors(c.fetchall())
            conn.close()


