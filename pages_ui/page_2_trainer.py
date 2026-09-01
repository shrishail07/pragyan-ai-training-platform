# import streamlit as st
# import pandas as pd
# from utils.db_helper import fetch_data, insert_data

# def render():
#     st.title("👨‍🏫 Expert Trainer Portal")
    
#     tab1, tab2, tab3 = st.tabs(["My Profile & EOI", "Current Demanded Skills", "My Assigned Classes"])
    
#     with tab1:
#         st.subheader("Step 1: Submit Profile")
#         with st.form("trainer_profile"):
#             name = st.text_input("Name")
#             email = st.text_input("Email", value=st.session_state.user_email)
#             exp = st.text_input("Experience (Years & Months)")
#             skills = st.text_input("Skills (Comma separated)")
#             avail = st.selectbox("Availability", ["Weekdays", "Weekends", "Both"])
#             if st.form_submit_button("Submit Profile"):
#                 insert_data("trainer_profiles", {"name": name, "email": email, "skills": skills, "experience": exp, "availability": avail, "status": "Pending"})
#                 st.success("Profile sent to Pragyan AI for approval!")
                
#         st.subheader("Step 3: Submit Expression of Interest (EOI)")
#         with st.form("eoi_form"):
#             topic = st.text_input("Topic")
#             # Enforce integer values on the frontend using step=1
#             price = st.number_input("Expected Price", min_value=0, step=1)
#             slot = st.text_input("Timing Slot")
#             if st.form_submit_button("Submit EOI"):
#                 # Explicitly cast to int() for the backend database insertion
#                 insert_data("trainer_eoi", {"trainer_email": st.session_state.user_email, "topic": topic, "price": int(price), "time_slot": slot, "status": "Pending"})
#                 st.success("EOI Submitted!")
                
#         # st.subheader("Step 3: Submit Expression of Interest (EOI)")
#         # with st.form("eoi_form"):
#         #     topic = st.text_input("Topic")
#         #     price = st.number_input("Expected Price")
#         #     slot = st.text_input("Timing Slot")
#         #     if st.form_submit_button("Submit EOI"):
#         #         insert_data("trainer_eoi", {"trainer_email": st.session_state.user_email, "topic": topic, "price": price, "time_slot": slot, "status": "Pending"})
#         #         st.success("EOI Submitted!")


    
#     with tab2:
#         st.subheader("Current Skill Programs Needed")
#         skills_list = ["Aptitude", "Communication", "DSA", "AI", "Data Science", "BI", "Machine Learning", "Deep Learning", "NLP", "LLM", "Computer Vision", "Data Analysis"]
#         for s in skills_list:
#             st.markdown(f"- {s}")
            
#     with tab3:
#         st.subheader("Assigned Classes (Approved Only)")
        
#         # Fetch all profiles matching the logged-in email
#         all_profiles = fetch_data("trainer_profiles")
#         my_profiles = [p for p in all_profiles if p.get('email') == st.session_state.user_email]
        
#         # Check if AT LEAST ONE of those profiles is "Approved"
#         is_approved = any(p.get('status') == "Approved" for p in my_profiles)
        
#         if is_approved:
#             classes = pd.DataFrame(fetch_data("trainer_classes"))
#             if not classes.empty:
#                 # Filter classes for this specific trainer
#                 my_classes = classes[classes['trainer_email'] == st.session_state.user_email]
#                 if not my_classes.empty:
#                     st.dataframe(my_classes)
#                 else:
#                     st.info("No classes assigned yet.")
#             else:
#                 st.info("No classes assigned yet.")
#         else:
#             st.warning("Your profile is pending approval from Pragyan AI Admin.")

import streamlit as st
import pandas as pd
from utils.db_helper import fetch_data, insert_data

def render():
    st.title("👨‍🏫 Expert Trainer Portal")
    
    tab1, tab2, tab3 = st.tabs(["My Profile & EOI", "Current Demanded Skills", "My Assigned Classes"])
    
    # Define the skills list globally so both tabs can access it
    skills_list = [
        "Aptitude", "Communication", "DSA", "AI", "Data Science", "BI", 
        "Machine Learning", "Deep Learning", "NLP", "LLM", "Computer Vision", "Data Analysis"
    ]
    
    with tab1:
        st.subheader("Step 1: Submit Profile")
        with st.form("trainer_profile"):
            name = st.text_input("Name")
            email = st.text_input("Email", value=st.session_state.user_email)
            exp = st.text_input("Experience (Years & Months)")
            skills = st.text_input("Skills (Comma separated)")
            avail = st.selectbox("Availability", ["Weekdays", "Weekends", "Both"])
            
            if st.form_submit_button("Submit Profile"):
                insert_data("trainer_profiles", {
                    "name": name, "email": email, "skills": skills, 
                    "experience": exp, "availability": avail, "status": "Pending"
                })
                st.success("Profile sent to Pragyan AI for approval!")
                
        st.subheader("Step 2: Submit Expression of Interest (EOI)")
        with st.form("eoi_form"):
            # Use multiselect populated by the demanded skills list
            selected_topics = st.multiselect("Select Topics of Interest", skills_list)
            price = st.number_input("Expected Price", min_value=0, step=1)
            slot = st.text_input("Timing Slot")
            
            if st.form_submit_button("Submit EOI"):
                if not selected_topics:
                    st.error("Please select at least one topic from the list.")
                else:
                    # Join selected skills into a single comma-separated string for the database
                    topic_string = ", ".join(selected_topics)
                    insert_data("trainer_eoi", {
                        "trainer_email": st.session_state.user_email, 
                        "topic": topic_string, 
                        "price": int(price), 
                        "time_slot": slot, 
                        "status": "Pending"
                    })
                    st.success("EOI Submitted successfully!")
    
    with tab2:
        st.subheader("Current Skill Programs Needed")
        for s in skills_list:
            st.markdown(f"- {s}")
            
    with tab3:
        st.subheader("Assigned Classes (Approved Only)")
        
        all_profiles = fetch_data("trainer_profiles")
        my_profiles = [p for p in all_profiles if p.get('email') == st.session_state.user_email]
        
        is_approved = any(p.get('status') == "Approved" for p in my_profiles)
        
        if is_approved:
            classes = pd.DataFrame(fetch_data("trainer_classes"))
            if not classes.empty:
                my_classes = classes[classes['trainer_email'] == st.session_state.user_email]
                if not my_classes.empty:
                    st.dataframe(my_classes)
                else:
                    st.info("No classes assigned yet.")
            else:
                st.info("No classes assigned yet.")
        else:
            st.warning("Your profile is pending approval from Pragyan AI Admin.")
