
# import streamlit as st

# def render():
#     st.title("Welcome to PRAGYAN AI")
#     st.subheader("Intelligent Training & Expert Management Platform")
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.info("Are you a Student?")
#         student_email = st.text_input("Student Email", placeholder="Enter your email", key="s_email")
#         if st.button("Student Login"):
#             if student_email:
#                 st.session_state.user_role = "student"
#                 st.session_state.user_email = student_email.strip()
#                 st.session_state.current_page = "student"
#                 st.rerun()
#             else:
#                 st.error("Please enter an email address.")
            
#     with col2:
#         st.success("Are you an Expert Trainer?")
#         trainer_email = st.text_input("Trainer Email", placeholder="Enter your email", key="t_email")
#         if st.button("Expert Trainer Login"):
#             if trainer_email:
#                 st.session_state.user_role = "trainer"
#                 st.session_state.user_email = trainer_email.strip()
#                 st.session_state.current_page = "trainer"
#                 st.rerun()
#             else:
#                 st.error("Please enter an email address.")
            
#     with col3:
#         st.warning("Pragyan AI Administration")
#         admin_pass = st.text_input("Admin Password", type="password")
#         if st.button("Admin Login"):
#             if admin_pass == "PRAGYANAI":
#                 st.session_state.user_role = "admin"
#                 st.session_state.current_page = "admin"
#                 st.rerun()
#             else:
#                 st.error("Incorrect Password!")

import streamlit as st

def render():
    st.title("Welcome to PRAGYAN AI")
    st.subheader("Intelligent Training & Expert Management Platform")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("Are you a Student?")
        student_email = st.text_input("Student Email", placeholder="Enter your email", key="s_email")
        if st.button("Student Login"):
            if student_email:
                st.session_state.user_role = "student"
                st.session_state.user_email = student_email.strip()
                st.session_state.current_page = "student"
                st.rerun()
            else:
                st.error("Please enter an email address.")
            
    with col2:
        st.success("Are you an Expert Trainer?")
        trainer_email = st.text_input("Trainer Email", placeholder="Enter your email", key="t_email")
        if st.button("Expert Trainer Login"):
            if trainer_email:
                st.session_state.user_role = "trainer"
                st.session_state.user_email = trainer_email.strip()
                st.session_state.current_page = "trainer"
                st.rerun()
            else:
                st.error("Please enter an email address.")
                
    with col3:
        st.info("Are you a Coordinator?")
        coord_email = st.text_input("Coordinator Email", placeholder="Enter your email", key="c_email")
        coord_pass = st.text_input("Password", type="password", key="c_pass")
        if st.button("Coordinator Login"):
            if coord_pass == "COORDINATOR" and coord_email:
                st.session_state.user_role = "coordinator"
                st.session_state.user_email = coord_email.strip()
                st.session_state.current_page = "coordinator"  # Ensure your main app.py routes this to page_4
                st.rerun()
            else:
                st.error("Invalid Email or Password!")
            
    with col4:
        st.warning("Pragyan AI Administration")
        admin_pass = st.text_input("Admin Password", type="password")
        if st.button("Admin Login"):
            if admin_pass == "PRAGYANAI":
                st.session_state.user_role = "admin"
                st.session_state.current_page = "admin"
                st.rerun()
            else:
                st.error("Incorrect Password!")
