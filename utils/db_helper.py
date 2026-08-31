import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

# Helper functions for clean API calls
def fetch_data(table_name):
    response = supabase.table(table_name).select("*").execute()
    return response.data

def insert_data(table_name, data_dict):
    response = supabase.table(table_name).insert(data_dict).execute()
    return response.data

def update_data(table_name, match_col, match_val, update_dict):
    response = supabase.table(table_name).update(update_dict).eq(match_col, match_val).execute()
    return response.data
