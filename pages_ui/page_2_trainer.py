import streamlit as st
import pandas as pd
from utils.db_helper import fetch_data, insert_data

def render():
    st.title("👨‍🏫 Expert Trainer Portal")
    
    tab1, tab2, tab3 = st.tabs(["My Profile & EOI", "Current Demanded Skills", "My Assigned Classes"])
    
    with tab1:
        st.subheader("Step 1: Submit Profile")
        with st.form("trainer_profile"):
            name = st.text_input("Name")
            email = st.text_input("Email", value=st.session_state.user_email)
            exp = st.text_input("Experience (Years & Months)")
            skills = st.text_input("Skills (Comma separated)")
            avail = st.selectbox("Availability", ["Weekdays", "Weekends", "Both"])
            if st.form_submit_button("Submit Profile"):
                insert_data("trainer_profiles", {"name": name, "email": email, "skills": skills, "experience": exp, "availability": avail, "status": "Pending"})
                st.success("Profile sent to Pragyan AI for approval!")
                
        st.subheader("Step 3: Submit Expression of Interest (EOI)")
        with st.form("eoi_form"):
            topic = st.text_input("Topic")
            price = st.number_input("Expected Price")
            slot = st.text_input("Timing Slot")
            if st.form_submit_button("Submit EOI"):
                insert_data("trainer_eoi", {"trainer_email": st.session_state.user_email, "topic": topic, "price": price, "time_slot": slot, "status": "Pending"})
                st.success("EOI Submitted!")
                
    with tab2:
        st.subheader("Current Skill Programs Needed")
        skills_list = ["Aptitude", "Communication", "DSA", "AI", "Data Science", "BI", "Machine Learning", "Deep Learning", "NLP", "LLM", "Computer Vision", "Data Analysis"]
        for s in skills_list:
            st.markdown(f"- {s}")
            
    with tab3:
        st.subheader("Assigned Classes (Approved Only)")
        # Fetch status
        profile = fetch_data("trainer_profiles")
        my_profile = [p for p in profile if p['email'] == st.session_state.user_email]
        
        if my_profile and my_profile[0].get('status') == "Approved":
            classes = pd.DataFrame(fetch_data("trainer_classes"))
            if not classes.empty:
                st.dataframe(classes[classes['trainer_email'] == st.session_state.user_email])
            else:
                st.info("No classes assigned yet.")
        else:
            st.warning("Your profile is pending approval from Pragyan AI Admin.")
