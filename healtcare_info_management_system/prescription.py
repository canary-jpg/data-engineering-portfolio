import streamlit as st 
from datetime import datetime
import database as db
import pandas as pd
import patient
import doctor

#function to verify prescription id
def verify_prescription_id(prescription_id):
    verify = False
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT id
            FROM prescription_record;
            """
        )
        for id in c.fetchall():
            if id[0] == prescription_id:
                verify = True
                break
            conn.close()
            return verify

#function to show prescription details given a list of prescriptions
def show_prescription_details(list_of_prescriptions):
    prescription_titles = ["Prescription ID", "Patient ID", "Patient name", "Doctor ID",
    "Doctor name", "Diagnosis", "Comments", "Medicine 1 name", "Medicine 1 dosage and description",
    "Medicine 2 name", "Medicine 2 dosage and description", "Medicine 3 name", "Medicine 3 dosage and description",] 
    if len(list_of_prescriptions) == 0:
        st.warning("No data to show")
    elif len(list_of_prescriptions) == 1:
        prescription_details = [x for x in list_of_prescriptions[0]]
        prescription_series = pd.Series(data = prescription_details, index = prescription_titles)
        st.write(prescription_series)
    else:
        prescription_details = []
        for prescription in list_of_prescriptions:
            prescription_details.append([x for x in prescription])
        df = pd.DataFrame(data = prescription_details, columns = prescription_titles)
        st.write(df)


#function to generate unique prescription id using current date and time
def generate_prescription_id():
    id_1 = datetime.now().strftime("%S%M%H")
    id_2 = datetime.now().strftime("%Y%m%d")[2:]
    id = f"RX-{id_1}-{id_2}"
    return id

#function fetches patient's name from database given their patient id
def get_patient_name(patient_id):
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT name
            FROM patient_record
            WHERE id = :id;
            """,
            {"id": patient_id}
        )
    return c.fetchone()[0]


#function that fetches doctor's name from database given their doctor id
def get_doctor_name(doctor_id):
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT name
            FROM doctor_record
            WHERE id = :id
            """,
            {"id": doctor_id}
        )
    return c.fetchone()[0]


#creating Prescription class containing fields and methods required to work with prescriptions table in database
class Prescription:
    def __init__(self):
        self.id = str()
        self.patient_id = str()
        self.patient_name = str()
        self.doctor_id = str()
        self.doctor_name = str()
        self.diagnosis = str()
        self.comments = str()
        self.medicine_1_name = str()
        self.medicine_1_dosage_desc = str()
        self.medicine_2_name = str()
        self.medicine_2_dosage_desc = str()
        self.medicine_3_name = str()
        self.medicine_3_dosage_desc = str()
    
    def add_prescription(self):
        st.write("Enter prescription details: ")
        patient_id = st.text_input("Patient ID")
        if patient_id == '':
            st.empty()
        elif not patient.verify_patient_id(patient_id):
            st.error("Invalid Patient ID")
        else:
            st.success("Verified")
            self.patient_id = patient_id
            self.patient_name = get_patient_name(patient_id)
        doctor_id = st.text_input("Doctor ID")
        if doctor_id == '':
            st.empty()
        elif not doctor.verify_doctor_id(doctor_id):
            st.error("Invalid Doctor ID")
        else:
            st.success("Verified")
            self.doctor_id = doctor_id
            self.doctor_name = get_doctor_name(doctor_id)
        self.diagnosis = st.text_area("Diagnosis")
        comments = st.text_area("Comments (if any)")
        self.comments = (lambda comment: None if comment == '' else comment)(comments)
        self.medicine_1_name = st.text_input("Medicine 1 name")
        self.medicine_1_dosage_desc = st.text_area("Medicine 1 dosage and description")
        med_2_name = st.text_input("Medicine 2 name")
        self.medicine_2_dosage_desc = (lambda med_2_name: None if med_2_name == '' else med_2_name)(med_2_name)
        med_2_dose_desc = st.text_area("Medicine 2 dosage  and description")
        self.medicine_2_dosage_desc = (lambda med_2_dose: None if med_2_dose == '' else med_2_dose)(med_2_dose_desc)
        med_3_name = st.text_input("Medicine 3 name")
        self.medicine_3_dosage_desc = (lambda med_3_name: None if med_3_name == '' else med_3_name)(med_3_name)
        med_3_dose_desc = st.text_area("Medicine 3 dosage  and description")
        self.medicine_3_dosage_desc = (lambda med_3_dose: None if med_3_dose == '' else med_3_dose)(med_3_dose_desc)
        self.id = generate_prescription_id()
        save = st.button("Save")

        if save:
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    INSERT INTO prescription_record
                    (
                        id, patient_id, patient_name, doctor_id,
                        doctor_name, diagnosis, comments,
                        medicine_1_name, medicine_1_dosage_desc,
                        medicine_2_name, medicine_2_dosage_desc,
                        medicine_3_name, medicine_3_dosage_desc
                    )
                    VALUES (
                        :rx_id, :pt_id, :pt_name, :dr_id, :dr_name,
                        :diag, :comments, :med_1_name, :med_1_dose,
                        :med_2_name, :med_2_dose, :med_3_name, :med_3_dose
                    );
                    """, 
                    {
                        "rx_id": self.id, "pt_id": self.patient_id, "pt_name": self.patient_name,
                        "dr_id": self.doctor_id, "dr_name": self.doctor_name, "diag": self.diagnosis,
                        "comments": self.comments, "med_1_name": self.medicine_1_name,
                        "med_1_dose": self.medicine_1_dosage_desc, "med_2_name": self.medicine_2_name,
                        "med_2_dose": self.medicine_2_dosage_desc, "med_3_name": self.medicine_3_name,
                        "med_3_dose": self.medicine_3_dosage_desc,
                    }
                )
            st.success("Prescription details saved successfully.")
            st.write("Prescription ID is: ", self.id)
            conn.close()


    def update_prescription(self):
        id = st.text_input("Enter Prescription ID for the prescription to be updated")
        if id == '':
            st.empty()
        elif not verify_prescription_id(id):
            st.error("Invalid Prescription ID")
        else:
            st.success("Verified")
            conn, c = db.connection()

            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM prescription_record
                    WHERE id = :id;
                    """,
                    {"id": id}
                )
                st.write("Here are the current details  of the prescription: ")
                show_prescription_details(c.fetchall())
            
        st.write("Enter new details of the prescription: ")
        self.diagnosis = st.text_area("Diagnosis")
        comments = st.text_area("Comments (in any)")
        self.commensts = (lambda comment: None if comment == '' else comment)(comments)
        self.medicine_1_name = st.text_input("Medicine 1 name")
        self.medicine_1_dosage_desc = st.text_area("Medicine 1 dosage and description")
        medicine_2_name = st.text_input("Medicine 2 name")
        self.medicine_2_name = (lambda med_2_name: None if med_2_name == '' else med_2_name)(medicine_2_name)
        medicine_3_name = st.text_input("Medicine 3 name")
        self.medicine_3_name = (lambda med_3_name: None if med_3_name == '' else med_3_name)(medicine_3_name)
        update = st.button("Update")

        if update:
            with conn:
                c.execute(
                    """
                    UPDATE prescription_record
                    SET diagnosis = :diag, comments = :comments,
                    medicine_1_name = :med_1_name, medicine_1_dosage_desc = :med_1_dose_desc,
                    medicine_2_name = :med_2_name, medicine_2_dosage_desc = :med_2_dose_desc,
                    medicine_3_name = :med_3_name, medicine_3_dosage_desc = :med_3_dose_desc
                    WHERE id = :id;
                    """,
                    {
                        "id": id, "diag": self.diagnosis, "comments": self.comments,
                        "med_1_name": self.medicine_1_name, "med_1_dose_desc": self.medicine_1_dosage_desc,
                        "med_2_name": self.medicine_2_name, "med_2_dose_desc": self.medicine_2_dosage_desc,
                        "med_3_name": self.medicine_3_name, "med_3_dose_desc": self.medicine_3_dosage_desc
                    }
                )
            st.success("Prescription details updated successfully.")
            conn.close()
    

    def delete_prescription(self):
        id = st.text_input("Enter Prescription ID of prescription to be deleted")
        if id == '':
            st.empty()
        elif not verify_prescription_id(id):
            st.error("Invalid ID")
        else:
            st.success("Verified")
            conn, c = db.connection()

            with conn:
                c.execute(
                    """ 
                    SELECT *
                    FROM prescription_record
                    WHERE id = :id;
                    """,
                    {"id": id}
                )
                st.write("Here are the details of the prescription to be deleted: ")
                show_prescription_details(c.fetchall())

                confirm = st.checkbox("Check this box to confirm deleted")
                if confirm:
                    delete = st.button("Delete")

                    if delete:
                        c.execute(
                            """
                            DELETE FROM prescription_record
                            WHERE id = :id
                            """,
                            {"id": id}
                        )
                        st.success("Prescription details successfully deleted.")
            conn.close()
    

    def prescriptions_by_patient(self):
        patient_id = st.text_input("Enter Patient ID to get the prescription records of a patient")
        if patient_id == '':
            st.empty()
        elif not patient.verify_patient_id(id):
            st.error("Invalid Patient ID")
        else:
            st.success("Verified")
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM prescription_record
                    WHERE patient_id = :pt_id;
                    """,
                    {"pt_id": patient_id}
                )
                st.write("Here are the prescription records of ", get_patient_name(patient_id), ":")
                show_prescription_details(c.fetchall())
            conn.close()



