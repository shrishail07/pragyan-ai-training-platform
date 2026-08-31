import streamlit as st
import pandas as pd
from utils.db_helper import fetch_data, insert_data

def render():
    st.title("🎓 Student Portal")
    
    # Check if student has accepted a proposal (mock logic for unlocking tabs)
    # In reality, fetch this from `student_custom_requests` status
    has_accepted_proposal = st.session_state.get("proposal_accepted", False)
    
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
                insert_data("student_profiles", {"email": st.session_state.user_email, "name": name, "college": college, "cgpa": cgpa, "dream_job": dream_job})
                st.success("Profile saved!")

    with tab1:
        st.subheader("Request Custom Skill Hours")
        st.write("Example: 'I want 3 hours data science skill in that 1 hr for python, 30 min for data analysis, 1 hr 30 min for ML.'")
        req = st.text_area("Detail your exact hour requirements for specific skills:")
        if st.button("Submit Request to Admin"):
            insert_data("student_custom_requests", {"student_email": st.session_state.user_email, "request_details": req, "status": "Pending"})
            st.success("Sent to Pragyan AI!")

    with tab2:
        st.subheader("Admin Proposals")
        st.info("If Pragyan AI has sent a customized curriculum proposal based on your request, it will appear here.")
        # Mock Accept Button
        if st.button("Accept Proposal"):
            st.session_state.proposal_accepted = True
            st.success("Proposal Accepted! Remaining tabs unlocked.")
            st.rerun()

    if has_accepted_proposal:
        with tab3:
            st.subheader("Programs in Planning Stage")
            planned = pd.DataFrame(fetch_data("programs_planned"))
            st.dataframe(planned)
            selected_prog = st.selectbox("Select Program ID to Join", planned['id'].tolist() if not planned.empty else [])
            if st.button("Join Program"):
                insert_data("student_enrollments", {"student_email": st.session_state.user_email, "program_id": selected_prog, "status": "Pending"})
                st.success("Join request sent to Admin!")
                
        with tab4:
            st.subheader("Programs I Joined (Yet to start)")
            enrolls = pd.DataFrame(fetch_data("student_enrollments"))
            if not enrolls.empty:
                my_enrolls = enrolls[enrolls['student_email'] == st.session_state.user_email]
                st.dataframe(my_enrolls)
                
        with tab5:
            st.subheader("Currently Running Programs")
            running = pd.DataFrame(fetch_data("programs_running"))
            st.dataframe(running)
    else:
        for t in [tab3, tab4, tab5]:
            with t:
                st.warning("Please submit and accept a proposal in Tab 2 to view this section.")
