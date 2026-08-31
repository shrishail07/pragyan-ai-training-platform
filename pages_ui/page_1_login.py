import streamlit as st

def render():
    st.title("Welcome to PRAGYAN AI")
    st.subheader("Intelligent Training & Expert Management Platform")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("Are you a Student?")
        if st.button("Student Login"):
            st.session_state.user_role = "student"
            # In a real app, you'd verify email/password here. For now, mock email:
            st.session_state.user_email = "student@example.com"
            st.session_state.current_page = "student"
            st.rerun()
            
    with col2:
        st.success("Are you an Expert Trainer?")
        if st.button("Expert Trainer Login"):
            st.session_state.user_role = "trainer"
            st.session_state.user_email = "trainer@example.com"
            st.session_state.current_page = "trainer"
            st.rerun()
            
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
