import streamlit as st
from pages_ui import page_0_admin, page_1_login, page_2_trainer, page_3_student, page_4_coordinator

st.set_page_config(page_title="PRAGYAN AI Platform", layout="wide")

# Initialize Session States
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Navigation Router
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

# Sidebar Navigation (only shown after login)
if st.session_state.current_page != "login":
    with st.sidebar:
        st.title("Navigation")
        if st.button("Logout"):
            st.session_state.current_page = "login"
            st.session_state.user_role = None
            st.rerun()
            
        if st.session_state.user_role == "student":
            if st.button("Student Dashboard"): navigate_to("student")
            if st.button("Coordinators Info"): navigate_to("coordinator")
        elif st.session_state.user_role == "trainer":
            if st.button("Trainer Dashboard"): navigate_to("trainer")
        elif st.session_state.user_role == "admin":
            if st.button("Admin Dashboard"): navigate_to("admin")

# Page Routing
if st.session_state.current_page == "login":
    page_1_login.render()
elif st.session_state.current_page == "admin":
    page_0_admin.render()
elif st.session_state.current_page == "trainer":
    page_2_trainer.render()
elif st.session_state.current_page == "student":
    page_3_student.render()
elif st.session_state.current_page == "coordinator":
    page_4_coordinator.render()
