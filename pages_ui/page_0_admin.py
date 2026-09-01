

import streamlit as st
import pandas as pd
from utils.db_helper import fetch_data, insert_data, update_data
from utils.helper_func import admin_filter


def render():
    st.title("⚙️ PRAGYAN AI - Admin Dashboard")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Planned Programs", "Running Programs", "Coordinators", "Trainer Approvals", "Student Approvals", "Assign Classes"
    ])
    
    with tab1:
        st.info("1.ADD Planned Programs")
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
            co_ordinator = col1.text_input("Event Co-ordinator")
            expert_trainer = col2.text_input("Expert Trainer")
            
            if st.form_submit_button("Commit Changes"):
                insert_data("programs_planned", {
                    "name": name, "skill_dept": skill, "duration_hrs": duration, 
                    "start_month": month, "time_slot": time, "price": price, 
                    "seats_available": seats, "batch_size": batch, "Event_Co_ordinator" :co_ordinator,
                    "Expert_Trainer":expert_trainer
                })
                st.success("Program Added!")
                
        st.error("2.Current Planned Programs")
        planned_data = fetch_data("programs_planned")
        
        if planned_data:
            planned_df = pd.DataFrame(planned_data)
            st.dataframe(planned_df)
            
            st.write("---")
            st.warning("3.Modify Existing Program (Current Planned Programs)")
            
            # Select ID outside the form to pre-fill the values dynamically
            selected_id = st.selectbox("Select Program ID to Modify:", planned_df['id'].tolist())
            
            # Extract current data for the selected ID
            current_prog = planned_df[planned_df['id'] == selected_id].iloc[0]
            
            # Safe index lookups for selectboxes
            skill_opts = ["Aptitude", "Data Science", "Machine Learning", "LLM"]
            time_opts = ["Weekdays", "Weekends"]
            curr_skill_idx = skill_opts.index(current_prog['skill_dept']) if current_prog['skill_dept'] in skill_opts else 0
            curr_time_idx = time_opts.index(current_prog['time_slot']) if current_prog['time_slot'] in time_opts else 0
            
            with st.form("update_planned_form"):
                col_mod1, col_mod2 = st.columns(2)
                mod_name = col_mod1.text_input("Program Name", value=current_prog['name'])
                mod_skill = col_mod1.selectbox("Skill Dept", skill_opts, index=curr_skill_idx)
                mod_duration = col_mod1.number_input("Duration (Hours)", min_value=1, value=int(current_prog['duration_hrs']))
                mod_month = col_mod2.text_input("Start Month", value=current_prog['start_month'])
                mod_time = col_mod2.selectbox("Time", time_opts, index=curr_time_idx)
                mod_price = col_mod2.number_input("Price (INR)", min_value=0, value=int(current_prog['price']))
                mod_seats = col_mod1.number_input("Seats Available", min_value=1, value=int(current_prog['seats_available']))
                mod_batch = col_mod2.number_input("Planned Batch Size", min_value=1, value=int(current_prog['batch_size']))
                mod_coord = col_mod1.text_input("Event Co-ordinator", value=current_prog.get('Event_Co_ordinator', ''))
                mod_trainer = col_mod2.text_input("Expert Trainer", value=current_prog.get('Expert_Trainer', ''))
                
                if st.form_submit_button("Update Program"):
                    update_data("programs_planned", "id", selected_id, {
                        "name": mod_name,
                        "skill_dept": mod_skill,
                        "duration_hrs": mod_duration,
                        "start_month": mod_month,
                        "time_slot": mod_time,
                        "price": mod_price,
                        "seats_available": mod_seats,
                        "batch_size": mod_batch,
                        "Event_Co_ordinator": mod_coord,
                        "Expert_Trainer": mod_trainer
                    })
                    st.success(f"Program ID {selected_id} updated successfully!")
                    st.rerun()


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
        st.subheader("1.Expert Trainer EOI & Approvals")
        trainers_data = fetch_data("trainer_profiles")
        st.markdown("ALL Expert Trainer EOI & Approvals Data")
        trainers = pd.DataFrame(trainers_data)
        st.dataframe(trainers)

        if not trainers.empty:
            st.divider()
            st.subheader("Manage Trainer Approval Status")
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

        trainers_data1 = fetch_data("trainer_profiles")
        trainers1 = pd.DataFrame(trainers_data1)
        
        st.header("2.You Can Filter The Data By (Name, Email, Skill)")

        fil_by_name = st.text_input("Filter by Name:")
        fil_by_email = st.text_input("Filter by Email:")
        fil_by_skill = st.text_input("Filter by Skill:")
        fil_by_status = st.text_input("Filter by Status:")

        result_df = admin_filter(
            trainers1,
            fil_by_name,
            fil_by_email,
            fil_by_skill,
            fil_by_status
        )

        st.dataframe(result_df)
        
    with tab5:
        st.subheader("Student Custom Requests")
        custom_reqs_data = fetch_data("student_custom_requests")
        custom_reqs = pd.DataFrame(custom_reqs_data)
        st.dataframe(custom_reqs)
        
        if not custom_reqs.empty:
            st.write("---")
            st.write("**Manage Custom Request Proposals**")
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                sel_req_id = st.selectbox("Select Request ID:", custom_reqs['id'].tolist(), key="req_select")
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Send Proposal"):
                    update_data("student_custom_requests", "id", sel_req_id, {"status": "Proposal Sent"})
                    st.success(f"Proposal sent for Request ID {sel_req_id}!")
                    st.rerun()
            with col3:
                st.write("")
                st.write("")
                if st.button("❌ Reject Request"):
                    update_data("student_custom_requests", "id", sel_req_id, {"status": "Rejected"})
                    st.error(f"Request ID {sel_req_id} Rejected.")
                    st.rerun()

        st.divider()
        
        st.subheader("Student Program Enrollments")
        enrolls_data = fetch_data("student_enrollments")
        enrolls = pd.DataFrame(enrolls_data)
        st.dataframe(enrolls)
        
        if not enrolls.empty:
            st.write("---")
            st.write("**Manage Enrollment Status**")
            col4, col5, col6 = st.columns([2, 1, 1])
            with col4:
                sel_enroll_id = st.selectbox("Select Enrollment ID:", enrolls['id'].tolist(), key="enroll_select")
            with col5:
                st.write("")
                st.write("")
                if st.button("✅ Approve Student"):
                    update_data("student_enrollments", "id", sel_enroll_id, {"status": "Approved"})
                    st.success(f"Enrollment ID {sel_enroll_id} Approved!")
                    st.rerun()
            with col6:
                st.write("")
                st.write("")
                if st.button("❌ Reject Student"):
                    update_data("student_enrollments", "id", sel_enroll_id, {"status": "Rejected"})
                    st.error(f"Enrollment ID {sel_enroll_id} Rejected.")
                    st.rerun()

    with tab6:
        st.subheader("Assign Tasks to Approved Trainers")
        
        # Only fetch trainers that have been approved
        trainers_data = fetch_data("trainer_profiles")
        approved_trainers = [t for t in (trainers_data or []) if t.get("status") == "Approved"]
        
        if not approved_trainers:
            st.warning("No approved trainers available. Please approve a trainer in Tab 4 first.")
        else:
            trainer_emails = [t["email"] for t in approved_trainers]
            
            with st.form("assign_class_form"):
                col1, col2 = st.columns(2)
                selected_trainer = col1.selectbox("Select Trainer (Email)", trainer_emails)
                event_name = col2.text_input("Event / Class Name")
                coord_name = col1.text_input("Coordinator Name")
                class_date = col2.text_input("Date (YYYY-MM-DD)")
                class_time = col1.text_input("Time (e.g., 10:00 AM)")
                
                if st.form_submit_button("Assign Task"):
                    insert_data("trainer_classes", {
                        "trainer_email": selected_trainer,
                        "event_name": event_name,
                        "coordinator_name": coord_name,
                        "date": class_date,
                        "time": class_time,
                        "attendance": "Pending",
                        "completed": "No",
                        "payment_status": "Pending"
                    })
                    st.success(f"Class assigned successfully to {selected_trainer}!")
            
            st.divider()
            st.subheader("Current Assignments")
            assigned_data = fetch_data("trainer_classes")
            
            if assigned_data:
                assigned_df = pd.DataFrame(assigned_data)
                st.dataframe(assigned_df)
                
                st.write("---")
                st.write("**Modify Assignment Status**")
                
                col_mod1, col_mod2, col_mod3, col_mod4 = st.columns(4)
                with col_mod1:
                    mod_id = st.selectbox("Select Class ID:", assigned_df['id'].tolist(), key="mod_class_id")
                with col_mod2:
                    mod_att = st.selectbox("Attendance", ["Pending", "Present", "Absent"], key="mod_att")
                with col_mod3:
                    mod_comp = st.selectbox("Completed", ["No", "Yes"], key="mod_comp")
                with col_mod4:
                    mod_pay = st.selectbox("Payment Status", ["Pending", "Processing", "Paid"], key="mod_pay")
                
                if st.button("Update Class Status"):
                    update_data("trainer_classes", "id", mod_id, {
                        "attendance": mod_att,
                        "completed": mod_comp,
                        "payment_status": mod_pay
                    })
                    st.success(f"Class ID {mod_id} updated successfully!")
                    st.rerun()
