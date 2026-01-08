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

# --- PROFESSIONAL STYLING (FIXING LINE & CENTERING) ---
st.markdown("""
    <style>
    /* 1. Sidebar Background & Removing the Black Line */
    [data-testid="stSidebar"] {
        background-color: #fcfcfc;
        border-right: none !important; /* Hides the vertical line */
    }
    
    /* 2. Logo Styling */
    .brand-title {
        font-family: 'Arial Black', sans-serif;
        font-size: 50px;
        font-weight: 900;
        color: #000000;
        text-align: center;
        margin-bottom: 0px;
        line-height: 1.1;
    }
    .brand-subtitle {
        font-size: 14px;
        color: #666;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 30px;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    /* 3. Centering the Category Title */
    .category-title {
        font-size: 15px;
        font-weight: bold;
        color: #444;
        margin-bottom: 20px;
        text-align: center; /* Centers the text */
        display: block;
        width: 100%;
    }

    /* 4. Button Styling */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 52px;
        font-weight: 600;
        font-size: 14px;
        background-color: #ffffff;
        color: #333;
        border: 1px solid #eeeeee;
        margin-bottom: 10px;
        box-shadow: 0px 1px 3px rgba(0,0,0,0.02);
    }
    div.stButton > button:hover {
        border-color: #000;
        background-color: #fdfdfd;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR MENU ---
with st.sidebar:
    st.markdown('<div class="brand-title">BROBOND</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">A Brand by SNBPL</div>', unsafe_allow_html=True)
    st.write("---")
    
    # Centered Category Label
    st.markdown('<div class="category-title">📋 MAIN CATEGORIES</div>', unsafe_allow_html=True)
    
    if "page" not in st.session_state: st.session_state.page = "Dashboard"

    if st.button("📊 SALES DASHBOARD"): st.session_state.page = "Dashboard"
    if st.button("📞 LEADS DATA"): st.session_state.page = "Leads"
    if st.button("📥 BULK IMPORT"): st.session_state.page = "Import"
    if st.button("💸 EXPENSES"): st.session_state.page = "Expenses"
    if st.button("👤 AYUSH BROBOND (HRM)"): st.session_state.page = "HRM"
    if st.button("👑 HIMANSHU BROBOND (CEO)"): st.session_state.page = "CEO"

# --- MAIN PAGE CONTENT ---
if st.session_state.page == "Dashboard":
    st.markdown('## 📍 SALES DASHBOARD')
    st.info("Bhai, DASHBOARD panel live hai!")

elif st.session_state.page == "Leads":
    st.markdown('## 📞 MASTER LEAD DATABASE')
    df = pd.read_csv(DATA_FILE)
    search = st.text_input("🔍 Search Leads...")
    if search:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    st.dataframe(df, use_container_width=True)

elif st.session_state.page == "Import":
    st.markdown('## 📥 BULK DATA IMPORT')
    prod = st.text_input("Product Category Name")
    file = st.file_uploader("Upload Excel", type=["xlsx"])
    if file and prod:
        if st.button("SAVE DATA"):
            new_data = pd.read_excel(file)
            new_data["Product Category"] = prod
            master = pd.read_csv(DATA_FILE)
            pd.concat([master, new_data], ignore_index=True).to_csv(DATA_FILE, index=False)
            st.success("Done!")
            st.balloons()
else:
    st.write(f"### {st.session_state.page} section coming soon.")
