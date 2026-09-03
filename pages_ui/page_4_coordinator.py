


# import streamlit as st
# import pandas as pd
# import json
# import PyPDF2
# from utils.db_helper import fetch_data, insert_data
# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate

# def extract_content_with_groq(text):
#     # Safety truncation: Limit to ~3,500 tokens to bypass Groq rate limits
#     safe_text = text[:15000]
    
#     # Initialize LangChain Groq model
#     llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0, api_key=st.secrets["GROQ_API_KEY"])
    
#     prompt = PromptTemplate.from_template(
#         "You are an AI curriculum assistant. Extract details from the text below.\n"
#         "Return strictly a valid JSON object with these exact keys: 'program_name', 'skills' (comma separated), 'full_syllabus'.\n"
#         "CRITICAL INSTRUCTION FOR 'full_syllabus': Format the content strictly as a detailed, Day-wise and Hour-by-Hour schedule based on the text.\n"
#         "Do not include markdown blocks like ```json or any other surrounding text. Return ONLY the raw JSON object.\n\n"
#         "Text:\n{text}"
#     )
    
#     chain = prompt | llm
    
#     try:
#         response = chain.invoke({"text": safe_text})
#         content = response.content.strip()
        
#         # Safely clean markdown formatting if the LLM accidentally includes it
#         if content.startswith("```json"):
#             content = content[7:-3]
#         elif content.startswith("```"):
#             content = content[3:-3]
            
#         return json.loads(content.strip())
#     except Exception as e:
#         st.error(f"Groq Extraction Failed: {str(e)}")
#         return None

# def render():
#     st.title("🤝 Program Coordinator Portal")
    
#     # Initialize session state to hold the draft before publishing
#     if "draft_syllabus" not in st.session_state:
#         st.session_state.draft_syllabus = None
        
#     tab1, tab2 = st.tabs(["Submit Details", "My Assigned Events & Syllabi"])
    
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
#         my_profile = [c for c in (all_coords or []) if c.get('email') == st.session_state.get('user_email')]
        
#         if not my_profile:
#             st.warning("Please submit your details in Tab 1 first.")
#         else:
#             profile = my_profile[-1] 
#             if profile.get('status') == 'Approved':
#                 my_name = profile.get('name')
#                 st.success(f"Welcome, {my_name}! Here are your assigned programs:")
                
#                 planned_data = fetch_data("programs_planned")
#                 running_data = fetch_data("programs_running")
#                 assigned_program_names = []
                
#                 if planned_data:
#                     planned_df = pd.DataFrame(planned_data)
#                     if 'Event_Co_ordinator' in planned_df.columns:
#                         my_planned = planned_df[planned_df['Event_Co_ordinator'] == my_name]
#                         st.write("**Upcoming Planned Programs:**")
#                         st.dataframe(my_planned)
#                         assigned_program_names.extend(my_planned['name'].tolist())
                        
#                 if running_data:
#                     running_df = pd.DataFrame(running_data)
#                     if 'Event_Co_ordinator' in running_df.columns:
#                         my_running = running_df[running_df['Event_Co_ordinator'] == my_name]
#                         st.write("**Currently Running Programs:**")
#                         st.dataframe(my_running)
#                         assigned_program_names.extend(my_running['name'].tolist())
                
#                 st.divider()
#                 st.info("Upload & Generate AI Syllabus")
                
#                 if assigned_program_names:
#                     sel_prog = st.selectbox("Select Program to Generate Syllabus:", list(set(assigned_program_names)))
#                     uploaded_file = st.file_uploader("Upload PDF Syllabus Draft", type=["pdf"])
                    
#                     if st.button("Generate Draft Syllabus") and uploaded_file is not None:
#                         with st.spinner("Extracting hour-by-hour curriculum via Groq LLM..."):
#                             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#                             raw_text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
                            
#                             ai_data = extract_content_with_groq(raw_text)
                            
#                             if ai_data:
#                                 # Save to session state instead of database so user can review it
#                                 st.session_state.draft_syllabus = ai_data
#                                 st.rerun()
                                
#                     # If an AI draft exists in memory, display the editor form
#                     if st.session_state.draft_syllabus:
#                         st.write("---")
#                         st.info("📝 Review and modify the AI-generated schedule before publishing.")
#                         draft = st.session_state.draft_syllabus
                        
#                         with st.form("finalize_syllabus_form"):
#                             mod_skills = st.text_input("Extracted Skills", value=str(draft.get('skills', '')))
#                             mod_syllabus = st.text_area("Hour-by-Hour Schedule", value=str(draft.get('full_syllabus', '')), height=400)
                            
#                             if st.form_submit_button("Publish Final Syllabus"):
#                                 insert_data("program_syllabi", {
#                                     "program_name": sel_prog,
#                                     "coordinator_name": my_name,
#                                     "extracted_skills": mod_skills,
#                                     "full_syllabus": mod_syllabus
#                                 })
#                                 # Clear the draft so the form closes
#                                 st.session_state.draft_syllabus = None
#                                 st.cache_data.clear()
#                                 st.success(f"Syllabus for {sel_prog} successfully published to students!")
#                                 st.rerun()
#                 else:
#                     st.info("You must be assigned to a program by the Admin before uploading a syllabus.")
#             else:
#                 st.warning("Your profile is currently pending approval from the Admin.")

import streamlit as st
import pandas as pd
import json
import time
import PyPDF2
from utils.db_helper import fetch_data, insert_data, update_data
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# 1. Syllabus Extraction
def extract_content_with_groq(text):
    safe_text = text[:15000]
    llm = ChatGroq(model="llama3-8b-8192", temperature=0, api_key=st.secrets["GROQ_API_KEY"])
    
    prompt = PromptTemplate.from_template(
        "You are an AI curriculum assistant. Extract details from the text below.\n"
        "Return strictly a valid JSON object with these exact keys: 'program_name', 'skills' (comma separated), 'full_syllabus'.\n"
        "CRITICAL INSTRUCTION FOR 'full_syllabus': Format the content strictly as a detailed schedule.\n"
        "Do not include markdown blocks like ```json or any other surrounding text. Return ONLY the raw JSON object.\n\n"
        "Text:\n{text}"
    )
    
    chain = prompt | llm
    try:
        response = chain.invoke({"text": safe_text})
        content = response.content.strip()
        if content.startswith("```json"): content = content[7:-3]
        elif content.startswith("```"): content = content[3:-3]
        return json.loads(content.strip())
    except Exception as e:
        st.error(f"Groq Extraction Failed: {str(e)}")
        return None

# 2. Module Generation
def generate_modules_with_groq(syllabus_text):
    safe_text = syllabus_text[:15000]
    llm = ChatGroq(model="llama3-8b-8192", temperature=0.2, api_key=st.secrets["GROQ_API_KEY"])
    
    prompt = PromptTemplate.from_template(
        "You are an expert technical curriculum designer. Analyze the following syllabus and break it down into logical Modules.\n"
        "Return STRICTLY a JSON ARRAY of objects. Each object must have these exact keys: 'module_name' (string), 'sessions_count' (integer), and 'content' (string - a 2 sentence summary of what is covered).\n"
        "Do not include markdown blocks or any other text. Output only the JSON array.\n\n"
        "Syllabus:\n{text}"
    )
    
    chain = prompt | llm
    try:
        response = chain.invoke({"text": safe_text})
        content = response.content.strip()
        if content.startswith("```json"): content = content[7:-3]
        elif content.startswith("```"): content = content[3:-3]
        return json.loads(content.strip())
    except Exception as e:
        st.error(f"Module Generation Failed: {str(e)}")
        return None

# 3. Notes Generation
def generate_notes_with_groq(module_name, module_content):
    llm = ChatGroq(model="llama3-8b-8192", temperature=0.4, api_key=st.secrets["GROQ_API_KEY"])
    
    prompt = PromptTemplate.from_template(
        "You are an expert educator. Create comprehensive study notes for a module titled '{module_name}'.\n"
        "Context about the module: {content}\n\n"
        "Return STRICTLY a JSON object with these exact keys:\n"
        "- 'pre_class': Things students should read or prepare before the session.\n"
        "- 'class_notes': Key concepts, definitions, and main topics to cover during the session.\n"
        "- 'post_class': Homework, assignments, or revision topics.\n"
        "Do not include markdown blocks or any other text. Output only the raw JSON object."
    )
    
    chain = prompt | llm
    try:
        response = chain.invoke({"module_name": module_name, "content": module_content})
        content = response.content.strip()
        if content.startswith("```json"): content = content[7:-3]
        elif content.startswith("```"): content = content[3:-3]
        return json.loads(content.strip())
    except Exception as e:
        return {"pre_class": "Failed to generate.", "class_notes": "Failed to generate.", "post_class": "Failed to generate."}

def render():
    st.title("🤝 Program Coordinator Portal")
    
    if "draft_syllabus" not in st.session_state:
        st.session_state.draft_syllabus = None
        
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
                st.cache_data.clear()
                st.success("Profile submitted to Pragyan AI Admin for approval!")
                
    with tab2:
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
                st.subheader("1. Upload & Generate AI Syllabus")
                
                if assigned_program_names:
                    sel_prog = st.selectbox("Select Program to Generate Syllabus:", list(set(assigned_program_names)))
                    uploaded_file = st.file_uploader("Upload PDF Syllabus Draft", type=["pdf"])
                    
                    if st.button("Generate Draft Syllabus") and uploaded_file is not None:
                        with st.spinner("Extracting curriculum via Groq LLM..."):
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            raw_text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
                            
                            ai_data = extract_content_with_groq(raw_text)
                            if ai_data:
                                st.session_state.draft_syllabus = ai_data
                                st.rerun()
                                
                    if st.session_state.draft_syllabus:
                        st.info("📝 Review and modify the AI-generated schedule before publishing.")
                        draft = st.session_state.draft_syllabus
                        
                        with st.form("finalize_syllabus_form"):
                            mod_skills = st.text_input("Extracted Skills", value=str(draft.get('skills', '')))
                            mod_syllabus = st.text_area("Hour-by-Hour Schedule", value=str(draft.get('full_syllabus', '')), height=400)
                            
                            if st.form_submit_button("Publish Final Syllabus"):
                                insert_data("program_syllabi", {
                                    "program_name": sel_prog,
                                    "coordinator_name": my_name,
                                    "extracted_skills": mod_skills,
                                    "full_syllabus": mod_syllabus
                                })
                                st.session_state.draft_syllabus = None
                                st.cache_data.clear()
                                st.success(f"Syllabus for {sel_prog} successfully published!")
                                st.rerun()

                st.divider()
                st.subheader("2. AI Module Planning & Note Generation")
                
                if assigned_program_names:
                    mod_prog_select = st.selectbox("Select Program to Manage Modules:", list(set(assigned_program_names)), key="mod_planner_select")
                    
                    # Ensure syllabus is published first
                    syllabi = fetch_data("program_syllabi")
                    my_syl = [s for s in (syllabi or []) if s.get('program_name') == mod_prog_select]
                    
                    if not my_syl:
                        st.warning("⚠️ You must generate and publish a Syllabus (Step 1) before creating modules.")
                    else:
                        all_modules = fetch_data("program_modules")
                        prog_modules = [m for m in (all_modules or []) if m.get('program_name') == mod_prog_select]
                        
                        # --- GENERATE MODULES ---
                        if not prog_modules:
                            st.info("No modules currently exist for this program.")
                            if st.button("🧠 AI: Generate Modules from Syllabus"):
                                with st.spinner("Breaking syllabus down into structured modules..."):
                                    ai_modules = generate_modules_with_groq(my_syl[-1]['full_syllabus'])
                                    if ai_modules:
                                        for mod in ai_modules:
                                            insert_data("program_modules", {
                                                "program_name": mod_prog_select,
                                                "coordinator_name": my_name,
                                                "module_name": str(mod.get("module_name", "Untitled")),
                                                "sessions_count": int(mod.get("sessions_count", 1)),
                                                "module_date": "",
                                                "status": "Inactive",
                                                "class_link": "",
                                                "content": str(mod.get("content", ""))
                                            })
                                        st.cache_data.clear()
                                        st.success("Modules structured successfully!")
                                        st.rerun()
                        else:
                            st.success(f"{len(prog_modules)} Modules Found. Manage schedule and notes below:")
                            
                            all_notes = fetch_data("module_notes")
                            
                            for m in prog_modules:
                                with st.expander(f"📦 {m['module_name']} | Sessions: {m['sessions_count']} | Status: {m.get('status', 'Inactive')}"):
                                    
                                    # Form to update Module Details (Dates, Status, Links)
                                    with st.form(f"update_mod_{m['id']}"):
                                        c1, c2, c3 = st.columns(3)
                                        mod_date = c1.text_input("Module Date (YYYY-MM-DD or Text)", value=str(m.get('module_date', '')))
                                        status_opts = ["Inactive", "Active (Running)", "Completed"]
                                        curr_stat_idx = status_opts.index(m.get('status')) if m.get('status') in status_opts else 0
                                        mod_stat = c2.selectbox("Status", status_opts, index=curr_stat_idx)
                                        mod_link = c3.text_input("Class Link", value=str(m.get('class_link', '')))
                                        
                                        if st.form_submit_button("Update Module Info"):
                                            update_data("program_modules", "id", m['id'], {
                                                "module_date": mod_date, "status": mod_stat, "class_link": mod_link
                                            })
                                            st.cache_data.clear()
                                            st.success("Module updated!")
                                            st.rerun()
                                            
                                    st.write("---")
                                    st.write("**AI Deep Notes Generation**")
                                    
                                    # Fetch existing notes for this specific module
                                    mod_notes = [n for n in (all_notes or []) if n.get('module_id') == m['id']]
                                    
                                    if not mod_notes:
                                        if st.button("Generate Pre/Post/Class Notes", key=f"gen_notes_{m['id']}"):
                                            with st.spinner(f"Drafting notes for {m['module_name']}..."):
                                                ai_notes = generate_notes_with_groq(m['module_name'], m['content'])
                                                insert_data("module_notes", {
                                                    "module_id": m['id'],
                                                    "pre_class": ai_notes.get('pre_class', ''),
                                                    "class_notes": ai_notes.get('class_notes', ''),
                                                    "post_class": ai_notes.get('post_class', '')
                                                })
                                                st.cache_data.clear()
                                                st.rerun()
                                    else:
                                        current_note = mod_notes[-1]
                                        with st.form(f"update_notes_{m['id']}"):
                                            pre_n = st.text_area("Pre-Class Notes", value=str(current_note.get('pre_class', '')), height=150)
                                            in_n = st.text_area("In-Class Notes", value=str(current_note.get('class_notes', '')), height=150)
                                            post_n = st.text_area("Post-Class Notes", value=str(current_note.get('post_class', '')), height=150)
                                            
                                            if st.form_submit_button("Save Notes Updates"):
                                                update_data("module_notes", "id", current_note['id'], {
                                                    "pre_class": pre_n, "class_notes": in_n, "post_class": post_n
                                                })
                                                st.cache_data.clear()
                                                st.success("Notes saved successfully!")
                                                st.rerun()
                else:
                    st.info("You must be assigned to a program by the Admin before managing modules.")
            else:
                st.warning("Your profile is currently pending approval from the Admin.")
