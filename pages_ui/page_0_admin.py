# import streamlit as st
# import pandas as pd
# from utils.db_helper import fetch_data, insert_data, update_data

# def render():
#     st.title("⚙️ PRAGYAN AI - Admin Dashboard")
    
#     tab1, tab2, tab3, tab4, tab5 = st.tabs([
#         "Planned Programs", "Running Programs", "Coordinators", "Trainer Approvals", "Student Approvals"
#     ])
    
#     with tab1:
#         st.subheader("Manage Planned Programs")
#         with st.form("add_planned"):
#             col1, col2 = st.columns(2)
#             name = col1.text_input("Program Name")
#             skill = col1.selectbox("Skill Dept", ["Aptitude", "Data Science", "Machine Learning", "LLM"])
#             duration = col1.number_input("Duration (Hours)", min_value=1)
#             month = col2.text_input("Start Month")
#             time = col2.selectbox("Time", ["Weekdays", "Weekends"])
#             price = col2.number_input("Price (INR)", min_value=0)
#             seats = col1.number_input("Seats Available", min_value=1)
#             batch = col2.number_input("Planned Batch Size", min_value=1)
#             if st.form_submit_button("Commit Changes"):
#                 insert_data("programs_planned", {
#                     "name": name, "skill_dept": skill, "duration_hrs": duration, 
#                     "start_month": month, "time_slot": time, "price": price, 
#                     "seats_available": seats, "batch_size": batch
#                 })
#                 st.success("Program Added!")
#         st.dataframe(pd.DataFrame(fetch_data("programs_planned")))

#     with tab2:
#         st.subheader("Manage Running Programs")
#         # Similar form as tab1 but for `programs_running`
#         st.dataframe(pd.DataFrame(fetch_data("programs_running")))
        
#     with tab3:
#         st.subheader("Program Coordinators")
#         # Similar form as tab1 but for `coordinators`
#         st.dataframe(pd.DataFrame(fetch_data("coordinators")))
        
#     with tab4:
#         st.subheader("Expert Trainer EOI & Approvals")
#         trainers = pd.DataFrame(fetch_data("trainer_profiles"))
#         st.dataframe(trainers)
#         # Logic to approve/reject would go here via update_data()
        
#     with tab5:
#         st.subheader("Student Requests & Enrollments")
#         reqs = pd.DataFrame(fetch_data("student_enrollments"))
#         st.dataframe(reqs)
#         # Logic to approve/reject student joins via update_data()
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
        
        planned_data = fetch_data("programs_planned")
        if planned_data:
            st.dataframe(pd.DataFrame(planned_data))

    with tab2:
        st.subheader("Manage Running Programs")
        with st.form("add_running"):
            col1, col2 = st.columns(2)
            name = col1.text_input("Course Name")
            duration = col1.text_input("Duration")
            skills = col2.text_input("Skills")
            link = col2.text_input("Class Link")
            if st.form_submit_button("Commit Changes"):
                insert_data("programs_running", {
                    "name": name, "duration": duration, "skills": skills, "class_link": link
                })
                st.success("Running Program Added!")
                
        running_data = fetch_data("programs_running")
        if running_data:
            st.dataframe(pd.DataFrame(running_data))
        
    with tab3:
        st.subheader("Program Coordinators")
        with st.form("add_coordinator"):
            col1, col2 = st.columns(2)
            prog_name = col1.text_input("Program Name")
            name = col2.text_input("Coordinator Name")
            email = col1.text_input("Email Id")
            phone = col2.text_input("Phone Number")
            exp = col1.text_input("Experience")
            cv = col2.text_input("CV Link")
            linkedin = col1.text_input("LinkedIn Profile")
            github = col2.text_input("GitHub Link")
            emp_id = col1.text_input("Employee ID")
            if st.form_submit_button("Commit Changes"):
                insert_data("coordinators", {
                    "program_name": prog_name, "name": name, "email": email, "phone": phone, 
                    "experience": exp, "cv_link": cv, "linkedin": linkedin, "github": github, "emp_id": emp_id
                })
                st.success("Coordinator Added!")
                
        coord_data = fetch_data("coordinators")
        if coord_data:
            st.dataframe(pd.DataFrame(coord_data))
        
    with tab4:
        st.subheader("Expert Trainer EOI & Approvals")
        trainers_data = fetch_data("trainer_profiles")
        trainers = pd.DataFrame(trainers_data)
        st.dataframe(trainers)
        
        if not trainers.empty:
            st.divider()
            st.subheader("Manage Trainer Status")
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                selected_id = st.selectbox("Select Trainer ID:", trainers['id'].tolist(), key="trainer_select")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Approve Trainer"):
                    update_data("trainer_profiles", "id", selected_id, {"status": "Approved"})
                    st.success(f"Trainer ID {selected_id} Approved!")
                    st.rerun()
            with col3:
                st.write("")
                st.write("")
                if st.button("❌ Reject Trainer"):
                    update_data("trainer_profiles", "id", selected_id, {"status": "Rejected"})
                    st.error(f"Trainer ID {selected_id} Rejected.")
                    st.rerun()
        
    with tab5:
        st.subheader("Student Requests & Enrollments")
        enrolls_data = fetch_data("student_enrollments")
        enrolls = pd.DataFrame(enrolls_data)
        st.dataframe(enrolls)
        
        if not enrolls.empty:
            st.divider()
            st.subheader("Manage Enrollment Status")
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                sel_enroll_id = st.selectbox("Select Enrollment ID:", enrolls['id'].tolist(), key="enroll_select")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Approve Student"):
                    update_data("student_enrollments", "id", sel_enroll_id, {"status": "Approved"})
                    st.success(f"Enrollment ID {sel_enroll_id} Approved!")
                    st.rerun()
            with col3:
                st.write("")
                st.write("")
                if st.button("❌ Reject Student"):
                    update_data("student_enrollments", "id", sel_enroll_id, {"status": "Rejected"})
                    st.error(f"Enrollment ID {sel_enroll_id} Rejected.")
                    st.rerun()
