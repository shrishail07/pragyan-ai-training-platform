
import streamlit as st
import pandas as pd
from utils.db_helper import fetch_data, insert_data, update_data

def render():
    st.title("🎓 Student Portal")
    
    tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Profile", "Custom Request", "Proposals", "Planned Programs", "My Joined Programs", "Running Programs"
    ])
    
    with tab0:
        st.subheader("Step 1: Student Profile")
        with st.form("student_profile"):
            name = st.text_input("Name")
            college = st.text_input("College Name")
            cgpa = st.number_input("Degree CGPA")
            dream_job = st.text_input("Dream Job Role")
            if st.form_submit_button("Save Profile"):
                insert_data("student_profiles", {
                    "email": st.session_state.user_email, 
                    "name": name, 
                    "college": college, 
                    "cgpa": cgpa, 
                    "dream_job": dream_job
                })
                st.success("Profile saved!")

    with tab1:
        st.subheader("Request Custom Skill Hours")
        st.write("Example: 'I want 3 hours data science skill in that 1 hr for python, 30 min for data analysis, 1 hr 30 min for ML.'")
        req = st.text_area("Detail your exact hour requirements for specific skills:")
        if st.button("Submit Request to Admin"):
            insert_data("student_custom_requests", {
                "student_email": st.session_state.user_email, 
                "request_details": req, 
                "status": "Pending"
            })
            st.success("Sent to Pragyan AI!")

    with tab2:
        st.subheader("Admin Proposals")
        
        # Fetch all custom requests
        reqs_data = fetch_data("student_custom_requests")
        
        # Filter for the logged-in student where the Admin has sent a proposal
        my_proposals = [
            r for r in (reqs_data or []) 
            if r.get("student_email") == st.session_state.user_email and r.get("status") == "Proposal Sent"
        ]
        
        if not my_proposals:
            st.info("If Pragyan AI has sent a customized curriculum proposal based on your request, it will appear here.")
        else:
            st.success("You have a new custom curriculum proposal from Pragyan AI!")
            df_proposals = pd.DataFrame(my_proposals)
            st.dataframe(df_proposals)
            
            st.divider()
            st.write("**Accept Your Proposal**")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                sel_prop_id = st.selectbox("Select Proposal ID:", df_proposals['id'].tolist())
            with col2:
                st.write("")
                st.write("")
                if st.button("✅ Accept Proposal"):
                    update_data("student_custom_requests", "id", sel_prop_id, {"status": "Accepted by Student"})
                    st.success("Proposal Accepted! Pragyan AI will schedule your class shortly.")
                    st.rerun()

    with tab3:
        st.subheader("Programs in Planning Stage")
        planned_data = fetch_data("programs_planned")
        
        if planned_data:
            planned = pd.DataFrame(planned_data)
            st.dataframe(planned)
            
            selected_planned = st.selectbox("Select Planned Program ID to Join", planned['id'].tolist(), key="join_planned_id")
            if st.button("Join Planned Program", key="btn_join_planned"):
                insert_data("student_enrollments", {
                    "student_email": st.session_state.user_email, 
                    "program_id": selected_planned, 
                    "program_type": "Planned",
                    "status": "Pending"
                })
                st.cache_data.clear()
                st.success("Join request sent to Admin!")
        else:
            st.info("No planned programs are available right now.")

        st.divider()

        st.info("Currently Running Programs")
        running_data = fetch_data("programs_running")
        
        if running_data:
            running = pd.DataFrame(running_data)
            st.dataframe(running)
            
            selected_running = st.selectbox("Select Running Program ID to Join", running['id'].tolist(), key="join_running_id")
            if st.button("Join Running Program", key="btn_join_running"):
                insert_data("student_enrollments", {
                    "student_email": st.session_state.user_email, 
                    "program_id": selected_running, 
                    "program_type": "Running",
                    "status": "Pending"
                })
                st.cache_data.clear()
                st.success("Join request sent to Admin!")
        else:
            st.warning("No running programs are available right now.")

    
    # with tab4:
    #     st.subheader("Programs I Joined")
    #     enrolls_data = fetch_data("student_enrollments")
        
    #     if enrolls_data:
    #         enrolls = pd.DataFrame(enrolls_data)
    #         my_enrolls = enrolls[enrolls['student_email'] == st.session_state.user_email]
            
    #         if not my_enrolls.empty:
    #             # Fallback for older database entries missing this column
    #             if 'program_type' not in my_enrolls.columns:
    #                 my_enrolls['program_type'] = "Planned"
                    
    #             planned_enrolls = my_enrolls[my_enrolls['program_type'] == 'Planned']
    #             running_enrolls = my_enrolls[my_enrolls['program_type'] == 'Running']
                
    #             st.write("**Planned Programs (Yet to start)**")
    #             if not planned_enrolls.empty:
    #                 st.dataframe(planned_enrolls)
    #             else:
    #                 st.info("You haven't joined any planned programs.")
                    
    #             st.write("---")
                
    #             st.write("**Currently Running Programs**")
    #             if not running_enrolls.empty:
    #                 st.dataframe(running_enrolls)
    #             else:
    #                 st.info("You haven't joined any running programs.")
    #         else:
    #             st.info("You haven't joined any programs yet.")
    #     else:
    #         st.info("You haven't joined any programs yet.")

    with tab4:
        st.subheader("Programs I Joined")
        enrolls_data = fetch_data("student_enrollments")
        
        if enrolls_data:
            enrolls = pd.DataFrame(enrolls_data)
            my_enrolls = enrolls[enrolls['student_email'] == st.session_state.user_email]
            
            if not my_enrolls.empty:
                # Fallback for older database entries missing this column
                if 'program_type' not in my_enrolls.columns:
                    my_enrolls['program_type'] = "Planned"
                
                # Standardize IDs to strings for accurate matching
                my_enrolls['program_id'] = my_enrolls['program_id'].astype(str)
                
                joined_planned = my_enrolls[my_enrolls['program_type'] == 'Planned']
                joined_running = my_enrolls[my_enrolls['program_type'] == 'Running']
                
                st.write("**Planned Programs (Yet to start)**")
                if not joined_planned.empty:
                    planned_data = fetch_data("programs_planned")
                    if planned_data:
                        planned_df = pd.DataFrame(planned_data)
                        planned_df['id_str'] = planned_df['id'].astype(str)
                        
                        # Filter full table by the joined IDs
                        my_planned_full = planned_df[planned_df['id_str'].isin(joined_planned['program_id'])]
                        
                        # Merge the enrollment status (Pending/Approved) to the display
                        my_planned_full = my_planned_full.merge(
                            joined_planned[['program_id', 'status']], 
                            left_on='id_str', 
                            right_on='program_id'
                        ).drop(columns=['id_str', 'program_id'])
                        
                        st.dataframe(my_planned_full)
                    else:
                        st.info("Program details are currently unavailable.")
                else:
                    st.info("You haven't joined any planned programs.")
                    
                st.write("---")
                
                st.write("**Currently Running Programs**")
                if not joined_running.empty:
                    running_data = fetch_data("programs_running")
                    if running_data:
                        running_df = pd.DataFrame(running_data)
                        running_df['id_str'] = running_df['id'].astype(str)
                        
                        # Filter full table by the joined IDs
                        my_running_full = running_df[running_df['id_str'].isin(joined_running['program_id'])]
                        
                        # Merge the enrollment status (Pending/Approved) to the display
                        my_running_full = my_running_full.merge(
                            joined_running[['program_id', 'status']], 
                            left_on='id_str', 
                            right_on='program_id'
                        ).drop(columns=['id_str', 'program_id'])
                        
                        st.dataframe(my_running_full)
                    else:
                        st.info("Program details are currently unavailable.")
                else:
                    st.info("You haven't joined any running programs.")
            else:
                st.info("You haven't joined any programs yet.")
        else:
            st.info("You haven't joined any programs yet.")
    
    with tab5:
        st.subheader("Currently Running Programs")
        running_data = fetch_data("programs_running")
        running = pd.DataFrame(running_data)
        
        if not running.empty:
            st.dataframe(running)
        else:
            st.info("No programs are currently running.")
            
        st.divider()
        st.subheader("📖 Course Syllabi & Skills")
        
        # Fetch the syllabi published by coordinators
        syllabi_data = fetch_data("program_syllabi")
        
        if syllabi_data:
            syllabi_df = pd.DataFrame(syllabi_data)
            
            # Extract unique program names for the dropdown
            available_programs = syllabi_df['program_name'].dropna().unique().tolist()
            
            if available_programs:
                selected_prog = st.selectbox("Select a Program to view its Syllabus:", available_programs)
                
                # Get the latest syllabus for the selected program
                prog_syllabus = syllabi_df[syllabi_df['program_name'] == selected_prog].iloc[-1]
                
                with st.container(border=True):
                    st.write(f"**Coordinator:** {prog_syllabus.get('coordinator_name', 'N/A')}")
                    st.write(f"**Target Skills:** {prog_syllabus.get('extracted_skills', 'N/A')}")
                    st.write("**Full Hour-by-Hour Syllabus:**")
                    # Using markdown/text area for clean display of multi-line schedules
                    st.markdown(prog_syllabus.get('full_syllabus', 'No detailed syllabus provided.'))
            else:
                st.info("No programs with published syllabi found.")
        else:
            st.info("No curriculum data has been published by the coordinators yet.")
