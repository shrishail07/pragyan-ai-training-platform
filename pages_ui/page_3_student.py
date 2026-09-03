
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

    # with tab3:
    #     st.subheader("Programs in Planning Stage")
    #     planned_data = fetch_data("programs_planned")
        
    #     if planned_data:
    #         planned = pd.DataFrame(planned_data)
    #         st.dataframe(planned)
            
    #         selected_prog = st.selectbox("Select Program ID to Join", planned['id'].tolist())
    #         if st.button("Join Program"):
    #             insert_data("student_enrollments", {
    #                 "student_email": st.session_state.user_email, 
    #                 "program_id": selected_prog, 
    #                 "status": "Pending"
    #             })
    #             st.success("Join request sent to Admin!")
    #     else:
    #         st.info("No planned programs are available right now.")

    #     st.divider()

    #     st.info("Currently Running Programs")
    #     running_data = fetch_data("programs_running")
        
    #     if running_data:
    #         running = pd.DataFrame(running_data)
    #         st.dataframe(running)
    #     else:
    #         st.warning("No running programs are available right now.")
    with tab3:
        st.subheader("Programs in Planning Stage")
        planned_data = fetch_data("programs_planned")
        
        if planned_data:
            planned = pd.DataFrame(planned_data)
            st.dataframe(planned)
            
            selected_prog = st.selectbox("Select Program ID to Join", planned['id'].tolist())
            if st.button("Join Program"):
                insert_data("student_enrollments", {
                    "student_email": st.session_state.user_email, 
                    "program_id": selected_prog, 
                    "status": "Pending"
                })
                st.success("Join request sent to Admin!")
        else:
            st.info("No planned programs are available right now.")

        # ALIGNMENT CHECK: These next lines must line up exactly with the 'if/else' above
        st.divider()

        st.info("Currently Running Programs")
        running_data = fetch_data("programs_running")
        
        if running_data:
            running = pd.DataFrame(running_data)
            st.dataframe(running)
        else:
            st.warning("No running programs are available right now.")

    
    with tab4:
        st.subheader("Programs I Joined (Yet to start)")
        enrolls_data = fetch_data("student_enrollments")
        enrolls = pd.DataFrame(enrolls_data)
        
        if not enrolls.empty:
            my_enrolls = enrolls[enrolls['student_email'] == st.session_state.user_email]
            if not my_enrolls.empty:
                st.dataframe(my_enrolls)
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
