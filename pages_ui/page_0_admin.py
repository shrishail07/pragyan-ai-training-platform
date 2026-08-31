import streamlit as st
import pandas as pd
from utils.db_helper import fetch_data, insert_data, update_data

def render():
    st.title("⚙️ PRAGYAN AI - Admin Dashboard")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Planned Programs", "Running Programs", "Coordinators", "Trainer Approvals", "Student Approvals"
    ])
    
    with tab1:
        st.subheader("Manage Planned Programs")
        with st.form("add_planned"):
            col1, col2 = st.columns(2)
            name = col1.text_input("Program Name")
            skill = col1.selectbox("Skill Dept", ["Aptitude", "Data Science", "Machine Learning", "LLM"])
            duration = col1.number_input("Duration (Hours)", min_value=1)
            month = col2.text_input("Start Month")
            time = col2.selectbox("Time", ["Weekdays", "Weekends"])
            price = col2.number_input("Price (INR)", min_value=0)
            seats = col1.number_input("Seats Available", min_value=1)
            batch = col2.number_input("Planned Batch Size", min_value=1)
            if st.form_submit_button("Commit Changes"):
                insert_data("programs_planned", {
                    "name": name, "skill_dept": skill, "duration_hrs": duration, 
                    "start_month": month, "time_slot": time, "price": price, 
                    "seats_available": seats, "batch_size": batch
                })
                st.success("Program Added!")
        st.dataframe(pd.DataFrame(fetch_data("programs_planned")))

    with tab2:
        st.subheader("Manage Running Programs")
        # Similar form as tab1 but for `programs_running`
        st.dataframe(pd.DataFrame(fetch_data("programs_running")))
        
    with tab3:
        st.subheader("Program Coordinators")
        # Similar form as tab1 but for `coordinators`
        st.dataframe(pd.DataFrame(fetch_data("coordinators")))
        
    with tab4:
        st.subheader("Expert Trainer EOI & Approvals")
        trainers = pd.DataFrame(fetch_data("trainer_profiles"))
        st.dataframe(trainers)
        # Logic to approve/reject would go here via update_data()
        
    with tab5:
        st.subheader("Student Requests & Enrollments")
        reqs = pd.DataFrame(fetch_data("student_enrollments"))
        st.dataframe(reqs)
        # Logic to approve/reject student joins via update_data()
