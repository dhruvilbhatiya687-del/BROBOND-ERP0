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

# --- PROFESSIONAL STYLING (MATCHING IMAGE 11) ---
st.markdown("""
    <style>
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #fcfcfc;
        border-right: 1px solid #e6e6e6;
    }
    
    /* Logo & Header Styling */
    .brand-title {
        font-family: 'Arial Black', Gadget, sans-serif;
        font-size: 55px;
        font-weight: 900;
        color: #000000;
        text-align: center;
        margin-bottom: 0px;
        line-height: 1;
    }
    .brand-subtitle {
        font-family: Arial, sans-serif;
        font-size: 16px;
        color: #666;
        text-align: center;
        margin-top: 0px;
        margin-bottom: 25px;
        font-weight: 600;
    }
    
    /* Sidebar Category Title */
    .category-title {
        font-size: 16px;
        font-weight: bold;
        color: #444;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* EXACT BUTTON STYLING FROM IMAGE 11 */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 55px;
        font-weight: 600;
        font-size: 15px;
        background-color: #ffffff;
        color: #333;
        border: 1px solid #e0e0e0;
        margin-bottom: 12px;
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        border-color: #000;
        background-color: #f9f9f9;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
    }
    
    .main-header {
        font-size: 42px;
        font-weight: 800;
        color: #1a1a1a;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR MENU (IMAGE 11 LAYOUT) ---
with st.sidebar:
    st.markdown('<div class="brand-title">BROBOND</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">A Brand by SNBPL</div>', unsafe_allow_html=True)
    st.write("---")
    
    st.markdown('<div class="category-title">📋 MAIN CATEGORIES</div>', unsafe_allow_html=True)
    
    if "page" not in st.session_state: st.session_state.page = "Dashboard"

    # Buttons
    if st.button("📊 SALES DASHBOARD"): st.session_state.page = "Dashboard"
    if st.button("📞 LEADS DATA"): st.session_state.page = "Leads"
    if st.button("📥 BULK IMPORT"): st.session_state.page = "Import"
    if st.button("💸 EXPENSES"): st.session_state.page = "Expenses"
    if st.button("👤 AYUSH BROBOND (HRM)"): st.session_state.page = "HRM"
    if st.button("👑 HIMANSHU BROBOND (CEO)"): st.session_state.page = "CEO"

# --- PAGE CONTENT ---
if st.session_state.page == "Dashboard":
    st.markdown('<div class="main-header">📍 SALES DASHBOARD</div>', unsafe_allow_html=True)
    st.info("Bhai, SALES DASHBOARD panel ab ekdum set hai!")

elif st.session_state.page == "Leads":
    st.markdown('<div class="main-header">📞 MASTER LEAD DATABASE</div>', unsafe_allow_html=True)
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        search = st.text_input("🔍 Search Leads...")
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.warning("No data found. Please import Excel first.")

elif st.session_state.page == "Import":
    st.markdown('<div class="main-header">📥 BULK DATA IMPORT</div>', unsafe_allow_html=True)
    p_name = st.text_input("Product Name")
    f = st.file_uploader("Upload Excel", type=["xlsx"])
    if f and p_name:
        if st.button("APPEND TO DATABASE"):
            new_df = pd.read_excel(f)
            new_df["Product Category"] = p_name
            master = pd.read_csv(DATA_FILE)
            pd.concat([master, new_df], ignore_index=True).to_csv(DATA_FILE, index=False)
            st.success("Done!")
            st.balloons()
else:
    st.markdown(f'<div class="main-header">📍 {st.session_state.page}</div>', unsafe_allow_html=True)
    st.write("Under Construction")
