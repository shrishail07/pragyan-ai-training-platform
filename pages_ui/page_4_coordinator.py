# import streamlit as st
# import pandas as pd
# from utils.db_helper import fetch_data

# def render():
#     st.title("🤝 Program Coordinators")
#     st.write("Find the coordinator details for your specific programs below.")
    
#     coordinators_data = fetch_data("coordinators")
    
#     if not coordinators_data:
#         st.info("Details will be coming soon...")
#     else:
#         df = pd.DataFrame(coordinators_data)
#         st.dataframe(df, use_container_width=True)
import streamlit as st
import pandas as pd
from utils.db_helper import fetch_data, insert_data

def render():
    st.title("🤝 Program Coordinator Portal")
    
    tab1, tab2 = st.tabs(["Submit Details", "My Assigned Events"])
    
    with tab1:
        st.subheader("Submit Coordinator Profile")
        with st.form("coord_profile_form"):
            col1, col2 = st.columns(2)
            name = col1.text_input("Full Name")
            email = col2.text_input("Email", value=st.session_state.get('user_email', ''))
            phone = col1.text_input("Phone Number")
            exp = col2.text_input("Experience (Years)")
            cv = col1.text_input("Resume Link (Google Drive PDF/Docx)")
            linkedin = col2.text_input("LinkedIn Profile")
            github = col1.text_input("GitHub Link")
            emp_id = col2.text_input("Employee ID")
            
            if st.form_submit_button("Submit Details"):
                insert_data("coordinators", {
                    "name": name, "email": email, "phone": phone,
                    "experience": exp, "cv_link": cv, "linkedin": linkedin,
                    "github": github, "emp_id": emp_id, "status": "Pending", "program_name": "Unassigned"
                })
                st.success("Profile submitted to Pragyan AI Admin for approval!")
                
    with tab2:
        st.subheader("My Assigned Events")
        
        all_coords = fetch_data("coordinators")
        # Find profile matching the logged-in email
        my_profile = [c for c in (all_coords or []) if c.get('email') == st.session_state.get('user_email')]
        
        if not my_profile:
            st.warning("Please submit your details in Tab 1 first.")
        else:
            profile = my_profile[-1] # Get latest submission
            if profile.get('status') == 'Approved':
                my_name = profile.get('name')
                st.success(f"Welcome, {my_name}! Here are your assigned programs:")
                
                planned_data = fetch_data("programs_planned")
                running_data = fetch_data("programs_running")
                
                if planned_data:
                    planned_df = pd.DataFrame(planned_data)
                    if 'Event_Co_ordinator' in planned_df.columns:
                        my_planned = planned_df[planned_df['Event_Co_ordinator'] == my_name]
                        st.write("**Upcoming Planned Programs:**")
                        st.dataframe(my_planned)
                        
                if running_data:
                    running_df = pd.DataFrame(running_data)
                    if 'Event_Co_ordinator' in running_df.columns:
                        my_running = running_df[running_df['Event_Co_ordinator'] == my_name]
                        st.write("**Currently Running Programs:**")
                        st.dataframe(my_running)
            else:
                st.warning("Your profile is currently pending approval from the Admin.")
