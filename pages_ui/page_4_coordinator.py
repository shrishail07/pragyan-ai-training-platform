

# import streamlit as st
# import pandas as pd
# from utils.db_helper import fetch_data, insert_data

# def render():
#     st.title("🤝 Program Coordinator Portal")
    
#     tab1, tab2 = st.tabs(["Submit Details", "My Assigned Events"])
    
#     with tab1:
#         st.subheader("Submit Coordinator Profile")
#         with st.form("coord_profile_form"):
#             col1, col2 = st.columns(2)
#             name = col1.text_input("Full Name")
#             email = col2.text_input("Email", value=st.session_state.get('user_email', ''))
#             phone = col1.text_input("Phone Number")
#             exp = col2.text_input("Experience (Years)")
#             cv = col1.text_input("Resume Link (Google Drive PDF/Docx)")
#             linkedin = col2.text_input("LinkedIn Profile")
#             github = col1.text_input("GitHub Link")
#             emp_id = col2.text_input("Employee ID")
            
#             if st.form_submit_button("Submit Details"):
#                 insert_data("coordinators", {
#                     "name": name, "email": email, "phone": phone,
#                     "experience": exp, "cv_link": cv, "linkedin": linkedin,
#                     "github": github, "emp_id": emp_id, "status": "Pending", "program_name": "Unassigned"
#                 })
#                 st.success("Profile submitted to Pragyan AI Admin for approval!")
                
#     with tab2:
#         st.subheader("My Assigned Events")
        
#         all_coords = fetch_data("coordinators")
#         # Find profile matching the logged-in email
#         my_profile = [c for c in (all_coords or []) if c.get('email') == st.session_state.get('user_email')]
        
#         if not my_profile:
#             st.warning("Please submit your details in Tab 1 first.")
#         else:
#             profile = my_profile[-1] # Get latest submission
#             if profile.get('status') == 'Approved':
#                 my_name = profile.get('name')
#                 st.success(f"Welcome, {my_name}! Here are your assigned programs:")
                
#                 planned_data = fetch_data("programs_planned")
#                 running_data = fetch_data("programs_running")
                
#                 if planned_data:
#                     planned_df = pd.DataFrame(planned_data)
#                     if 'Event_Co_ordinator' in planned_df.columns:
#                         my_planned = planned_df[planned_df['Event_Co_ordinator'] == my_name]
#                         st.write("**Upcoming Planned Programs:**")
#                         st.dataframe(my_planned)
                        
#                 if running_data:
#                     running_df = pd.DataFrame(running_data)
#                     if 'Event_Co_ordinator' in running_df.columns:
#                         my_running = running_df[running_df['Event_Co_ordinator'] == my_name]
#                         st.write("**Currently Running Programs:**")
#                         st.dataframe(my_running)
#             else:
#                 st.warning("Your profile is currently pending approval from the Admin.")


import streamlit as st
import pandas as pd
import json
import PyPDF2
from utils.db_helper import fetch_data, insert_data
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# def extract_content_with_groq(text):
#     # Initialize LangChain Groq model
#     llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0, api_key=st.secrets["GROQ_API_KEY"])
    
#     prompt = PromptTemplate.from_template(
#         "You are an AI curriculum assistant. Extract details from the text below.\n"
#         "Return strictly a valid JSON object with these exact keys: 'program_name', 'skills' (comma separated), 'full_syllabus'.\n"
#         "Do not include markdown blocks or any other text.\n\n"
#         "Text:\n{text}"
#     )
    
#     chain = prompt | llm
#     response = chain.invoke({"text": text})
    
#     try:
#         return json.loads(response.content)
#     except Exception as e:
#         st.error("Failed to parse the structured output from Groq.")
#         return None

def extract_content_with_groq(text):
    # Safety truncation: Limit to ~3,500 tokens to bypass Groq rate limits
    safe_text = text[:15000]
    
    # Initialize LangChain Groq model
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0, api_key=st.secrets["GROQ_API_KEY"])
    
    prompt = PromptTemplate.from_template(
        "You are an AI curriculum assistant. Extract details from the text below.\n"
        "Return strictly a valid JSON object with these exact keys: 'program_name', 'skills' (comma separated), 'full_syllabus'.\n"
        "Do not include markdown blocks or any other text.\n\n"
        "Text:\n{text}"
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"text": safe_text})
        return json.loads(response.content)
    except Exception as e:
        # Fallback error handling if the API still rejects or fails to parse
        st.error(f"Groq Extraction Failed: {str(e)}")
        return None


def render():
    st.title("🤝 Program Coordinator Portal")
    
    tab1, tab2 = st.tabs(["Submit Details", "My Assigned Events & Syllabi"])
    
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
        my_profile = [c for c in (all_coords or []) if c.get('email') == st.session_state.get('user_email')]
        
        if not my_profile:
            st.warning("Please submit your details in Tab 1 first.")
        else:
            profile = my_profile[-1] 
            if profile.get('status') == 'Approved':
                my_name = profile.get('name')
                st.success(f"Welcome, {my_name}! Here are your assigned programs:")
                
                planned_data = fetch_data("programs_planned")
                running_data = fetch_data("programs_running")
                assigned_program_names = []
                
                if planned_data:
                    planned_df = pd.DataFrame(planned_data)
                    if 'Event_Co_ordinator' in planned_df.columns:
                        my_planned = planned_df[planned_df['Event_Co_ordinator'] == my_name]
                        st.write("**Upcoming Planned Programs:**")
                        st.dataframe(my_planned)
                        assigned_program_names.extend(my_planned['name'].tolist())
                        
                if running_data:
                    running_df = pd.DataFrame(running_data)
                    if 'Event_Co_ordinator' in running_df.columns:
                        my_running = running_df[running_df['Event_Co_ordinator'] == my_name]
                        st.write("**Currently Running Programs:**")
                        st.dataframe(my_running)
                        assigned_program_names.extend(my_running['name'].tolist())
                
                st.divider()
                st.subheader("Upload & Generate AI Syllabus")
                
                if assigned_program_names:
                    sel_prog = st.selectbox("Select Program to Generate Syllabus:", list(set(assigned_program_names)))
                    uploaded_file = st.file_uploader("Upload PDF Syllabus Draft", type=["pdf"])
                    
                    if st.button("Generate & Publish Syllabus") and uploaded_file is not None:
                        with st.spinner("Extracting content via Groq LLM..."):
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            raw_text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
                            
                            ai_data = extract_content_with_groq(raw_text)
                            
                            if ai_data:
                                insert_data("program_syllabi", {
                                    "program_name": sel_prog,
                                    "coordinator_name": my_name,
                                    "extracted_skills": ai_data.get('skills', ''),
                                    "full_syllabus": ai_data.get('full_syllabus', '')
                                })
                                st.success(f"Syllabus for {sel_prog} successfully published to students!")
                else:
                    st.info("You must be assigned to a program by the Admin before uploading a syllabus.")
            else:
                st.warning("Your profile is currently pending approval from the Admin.")
