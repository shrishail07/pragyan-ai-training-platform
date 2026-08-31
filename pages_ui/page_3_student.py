# import streamlit as st
# import pandas as pd
# from utils.db_helper import fetch_data, insert_data

# def render():
#     st.title("🎓 Student Portal")
    
#     # Check if student has accepted a proposal (mock logic for unlocking tabs)
#     # In reality, fetch this from `student_custom_requests` status
#     has_accepted_proposal = st.session_state.get("proposal_accepted", False)
    
#     tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
#         "Profile", "Custom Request", "Proposals", "Planned Programs", "My Joined Programs", "Running Programs"
#     ])
    
#     with tab0:
#         st.subheader("Step 1: Student Profile")
#         with st.form("student_profile"):
#             name = st.text_input("Name")
#             college = st.text_input("College Name")
#             cgpa = st.number_input("Degree CGPA")
#             dream_job = st.text_input("Dream Job Role")
#             if st.form_submit_button("Save Profile"):
#                 insert_data("student_profiles", {"email": st.session_state.user_email, "name": name, "college": college, "cgpa": cgpa, "dream_job": dream_job})
#                 st.success("Profile saved!")

#     with tab1:
#         st.subheader("Request Custom Skill Hours")
#         st.write("Example: 'I want 3 hours data science skill in that 1 hr for python, 30 min for data analysis, 1 hr 30 min for ML.'")
#         req = st.text_area("Detail your exact hour requirements for specific skills:")
#         if st.button("Submit Request to Admin"):
#             insert_data("student_custom_requests", {"student_email": st.session_state.user_email, "request_details": req, "status": "Pending"})
#             st.success("Sent to Pragyan AI!")

#     with tab2:
#         st.subheader("Admin Proposals")
#         st.info("If Pragyan AI has sent a customized curriculum proposal based on your request, it will appear here.")
#         # Mock Accept Button
#         if st.button("Accept Proposal"):
#             st.session_state.proposal_accepted = True
#             st.success("Proposal Accepted! Remaining tabs unlocked.")
#             st.rerun()

#     if has_accepted_proposal:
# with tab3:
#         st.subheader("Programs in Planning Stage")
#         planned_data = fetch_data("programs_planned")
#         planned = pd.DataFrame(planned_data)
        
#         if not planned.empty:
#             st.dataframe(planned)
#             selected_prog = st.selectbox("Select Program ID to Join", planned['id'].tolist())
#             if st.button("Join Program"):
#                 insert_data("student_enrollments", {
#                     "student_email": st.session_state.user_email, 
#                     "program_id": selected_prog, 
#                     "status": "Pending"
#                 })
#                 st.success("Join request sent to Admin!")
#         else:
#             st.info("No planned programs are available right now.")
            
#     with tab4:
#         st.subheader("Programs I Joined (Yet to start)")
#         enrolls_data = fetch_data("student_enrollments")
#         enrolls = pd.DataFrame(enrolls_data)
        
#         if not enrolls.empty:
#             my_enrolls = enrolls[enrolls['student_email'] == st.session_state.user_email]
#             if not my_enrolls.empty:
#                 st.dataframe(my_enrolls)
#             else:
#                 st.info("You haven't joined any programs yet.")
#         else:
#             st.info("You haven't joined any programs yet.")
            
#     with tab5:
#         st.subheader("Currently Running Programs")
#         running_data = fetch_data("programs_running")
#         running = pd.DataFrame(running_data)
        
#         if not running.empty:
#             st.dataframe(running)
#         else:
#             st.info("No programs are currently running.")

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
        planned = pd.DataFrame(planned_data)
        
        if not planned.empty:
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
