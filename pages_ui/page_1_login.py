# import streamlit as st

# def render():
#     st.title("Welcome to PRAGYAN AI")
#     st.subheader("Intelligent Training & Expert Management Platform")
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.info("Are you a Student?")
#         if st.button("Student Login"):
#             st.session_state.user_role = "student"
#             # In a real app, you'd verify email/password here. For now, mock email:
#             st.session_state.user_email = "student@example.com"
#             st.session_state.current_page = "student"
#             st.rerun()
            
#     with col2:
#         st.success("Are you an Expert Trainer?")
#         if st.button("Expert Trainer Login"):
#             st.session_state.user_role = "trainer"
#             st.session_state.user_email = "trainer@example.com"
#             st.session_state.current_page = "trainer"
#             st.rerun()
            
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
    
    col1, col2, col3 = st.columns(3)
    
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
        st.warning("Pragyan AI Administration")
        admin_pass = st.text_input("Admin Password", type="password")
        if st.button("Admin Login"):
            if admin_pass == "PRAGYANAI":
                st.session_state.user_role = "admin"
                st.session_state.current_page = "admin"
                st.rerun()
            else:
                st.error("Incorrect Password!")
