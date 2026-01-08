import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="BROBOND ERP", page_icon="⚪", layout="wide")

# --- DATA SETUP ---
EXCEL_COLUMNS = [
    "Lead", "Owner", "First Name", "Last Name", "Email", 
    "Mobile Country Code", "Mobile", "Designation", 
    "Phone Country Code", "Phone", "Lead Source", "Sub Lead Source", 
    "Lead Status", "Industry", "Department", "Annual Revenue", 
    "Company Name", "Country", "State", "City", "Street", 
    "Pincode", "Lead Priority", "Description", "Product Category"
]
DATA_FILE = "leads_master.csv"

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=EXCEL_COLUMNS).to_csv(DATA_FILE, index=False)

# --- PROFESSIONAL STYLING (Look from 6.png) ---
st.markdown("""
    <style>
    .main-header { font-size: 36px; font-weight: bold; color: #1E293B; margin-bottom: 20px; }
    /* Sidebar Button Styling */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 60px;
        font-weight: 600;
        font-size: 16px;
        background-color: #FFFFFF;
        color: #1E293B;
        border: 1px solid #E2E8F0;
        margin-bottom: 10px;
        text-align: center;
    }
    div.stButton > button:hover {
        border-color: #000;
        background-color: #F8FAFC;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR MENU (Exact as your 6.png) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>BROBOND</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; margin-top: 0;'>A Brand by SNBPL</p>", unsafe_allow_html=True)
    st.write("---")
    st.write("📋 **MAIN CATEGORIES**")
    
    if "page" not in st.session_state: st.session_state.page = "Dashboard"

    if st.button("📊 SALES DASHBOARD"): st.session_state.page = "Dashboard"
    if st.button("📞 LEADS DATA"): st.session_state.page = "Leads"
    if st.button("📥 BULK IMPORT"): st.session_state.page = "Import"
    if st.button("💸 EXPENSES"): st.session_state.page = "Expenses"
    if st.button("👤 AYUSH BROBOND (HRM)"): st.session_state.page = "HRM"
    if st.button("👑 HIMANSHU BROBOND (CEO)"): st.session_state.page = "CEO"

# --- PAGE LOGIC ---
if st.session_state.page == "Dashboard":
    st.markdown('<div class="main-header">📍 SALES DASHBOARD</div>', unsafe_allow_html=True)
    st.info("Bhai, SALES DASHBOARD panel ab ekdum set hai!")

elif st.session_state.page == "Leads":
    st.markdown('<div class="main-header">📞 MASTER LEAD DATABASE</div>', unsafe_allow_html=True)
    df = pd.read_csv(DATA_FILE)
    search = st.text_input("🔍 Search by Name, Company, or City")
    if search:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    st.dataframe(df, use_container_width=True)

elif st.session_state.page == "Import":
    st.markdown('<div class="main-header">📥 BULK DATA IMPORT</div>', unsafe_allow_html=True)
    prod_name = st.text_input("Enter Product Category Name (e.g. Product A)")
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
    if uploaded_file and prod_name:
        temp_df = pd.read_excel(uploaded_file)
        temp_df["Product Category"] = prod_name
        if st.button("CONFIRM MERGE"):
            master_df = pd.read_csv(DATA_FILE)
            final_df = pd.concat([master_df, temp_df], ignore_index=True)
            final_df.to_csv(DATA_FILE, index=False)
            st.success("Bhai, data jud gaya!")
            st.balloons()

else:
    st.markdown(f'<div class="main-header">📍 {st.session_state.page}</div>', unsafe_allow_html=True)
    st.write("Section Under Construction")
