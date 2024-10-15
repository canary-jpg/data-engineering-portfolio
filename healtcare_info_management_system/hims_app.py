import streamlit as st 
import database as db
from patient import Patient
from department import Department
from doctor import Doctor
from prescription import Prescription
from medical_test import MedicalTest
import config
import sqlite3 as sql


#function to verify edit mode password
def verify_edit_mode_password():
    edit_mode_password = st.sidebar.text_input("Enter edit mode password", type = "password")
    if edit_mode_password == config.edit_mode_password:
        st.sidebar.success("Verified")
        return True
    elif edit_mode_password == '':
        st.empty()
    else:
        st.sidebar.error("Invalid edit mode password")
        return False


#function to verify doctor/medical lab scientist access code
def verify_dr_mls_access_code():
    dr_mls_access_code = st.sidebar.text_input("Enter doctor/medical lab scientist access code", type = "password")
    if dr_mls_access_code == config.dr_mls_access_code:
        st.sidebar.success("Verfied")
        return True
    elif dr_mls_access_code == '':
        st.empty()
    else:
        st.sidebar.error("Invalid access code")
        return False 


#function to perform various operations of the patient module
def patients():
    st.header("PATIENTS")
    option_list = ['', 'Add Patient', 'Update Patient', 'Remove Patient', 'Show Patient Records', 'Search Patients']
    option = st.sidebar.selectbox('Select Function', option_list)
    p = Patient()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_edit_mode_password():
        if option == option_list[1]:
            st.subheader("ADD PATIENT")
            p.add_patient()
        elif option == option_list[2]:
            st.subheader("UPDATE PATIENT INFO")
            p.update_patient()
        elif option == option_list[3]:
            st.subheader("REMOVE PATIENT")
            try:
                p.delete_patient()
            except sql.IntegrityError:
                st.error("This entry cannot be deleted as other records are using it.")
    elif option == option_list[4]:
        st.subheader("COMPLETE PATIENT RECORDS")
        p.show_all_patients()
    elif option == option_list[5]:
        st.subheader("SEARCH PATIENTS")
        p.search_patients()


#function to perform various operations of doctor module
def doctors():
    st.header("DOCTORS")
    option_list = ['', 'Add Doctor', 'Update Doctor Info', 'Delete Doctor Info', 'Show Complete Doctor Records', 'Search for Doctors']
    option = st.sidebar.selectbox("Select Function", option_list)
    dr = Doctor()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_edit_mode_password():
        if option == option_list[1]:
            st.subheader("ADD DOCTOR INFO")
            dr.add_doctor()
        elif option == option_list[2]:
            st.subheader("UPDATE DOCTOR INFO")
            dr.update_doctor()
        elif option == option_list[3]:
            st.subheader("REMOVE DOCTOR INFO")
            try:
                dr.delete_doctor()
            except sql.IntegrityError:
                st.error("This entry cannot be deleted as other records are using it.")
        elif option == option_list[4]:
            st.subheader("COMPLETE DOCTOR RECORDS")
            dr.show_all_doctors()
        elif option == option_list[5]:
            st.subheader("SEARCH FOR DOCTORS")
            dr.search_doctors()


#function to perform various operations of the prescription module
def prescriptions():
    st.header("PRESCRIPTIONS")
    option_list = ['', 'Add Prescription', 'Update Prescription Info', 'Delete Prescription', 'Show patient prescription(s)']
    option = st.sidebar.selectbox("Select Function", option_list)
    rx = Prescription()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_dr_mls_access_code():
        if option == option_list[1]:
            st.subheader("ADD PRESCRIPTION")
            rx.add_prescription()
        elif option == option_list[2]:
            st.subheader("UPDATE PRESCRIPTION INFO")
            rx.update_prescription()
        elif option == option_list[3]:
            st.subheader("DELETE PRESCRIPTION")
            rx.delete_prescription()
    elif option == option_list[4]:
        st.subheader("PATIENT PRESCRIPTION INFO")
        rx.prescriptions_by_patient()


#function to perform various operations of the medical test module
def medical_tests():
    st.header("MEDICAL TESTS")
    option_list = ['', 'Add Medical Test', 'Update Medical Test Info', 'Delete Medical Test', 'Show Patient Medical Test(s)']
    option = st.sidebar.selectbox("Select Function", option_list)
    t = MedicalTest()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_dr_mls_access_code():
        if option == option_list[1]:
            st.subheader("ADD MEDICAL TEST")
            t.add_medical_test()
        elif option == option_list[2]:
            st.subheader("UPDATE MEDICAL TEST INFO")
            t.update_medical_test()
        elif option == option_list[3]:
            st.subheader("DELETE MEDICAL TEST")
            t.delete_medical_test()
        else:
            st.subheader("SEARCH PATIENT MEDICAL TEST(S)")
            t.medical_test_by_patient()


#function to perform various operations of department module
def departments():
    st.header("DEPARTMENTS")
    option_list = ['', 'Add Department', 'Update Department', 'Delete Department', 'Show Department Records', 'Search Departments', 'Search Doctor by Department']
    option = st.sidebar.selectbox('Select Function', option_list)
    d = Department()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_edit_mode_password():
        if option == option_list[1]:
            st.subheader("ADD DEPARTMENT")
            d.add_department()
        elif option == option_list[2]:
            st.subheader("UPDATE DEPARTMENT INFO")
            d.update_department()
        elif option == option_list[3]:
            st.subheader("DELETE DEPARTMENT INFO")
            try:
                d.delete_department
            except sql.IntegrityError:
                st.error("This entry cannot be deleted as other records are using it.")
    elif option == option_list[4]:
        st.subheader("COMPLETE DEPARTMENT RECORDS")
        d.show_all_departments()
    else:
        st.subheader("DOCTORS BY DEPARTMENT")
        d.list_dept_doctors()


#function to implement and initialize home/main menu on successful authentication
def home():
    db.initialize_db()
    option = st.sidebar.selectbox('Select Module', ['', 'Patients', 'Doctors', 'Prescriptions', 'Medical Tests', 'Departments'])
    if option == 'Patients':
        patients()
    elif option == 'Doctors':
        doctors()
    elif option == 'Prescriptions':
        prescriptions()
    elif option == 'Medical Tests':
        medical_tests()
    else:
        departments()
    
st.title("HEALTHCARE INFORMATION MANAGEMENT SYSTEM")
password = st.sidebar.text_input('Enter password', type = 'password')
if password == config.password:
    st.sidebar.success('Verified')
    home()
elif password == '':
    st.empty()
else:
    st.sidebar.error("Invalid password")
        

        