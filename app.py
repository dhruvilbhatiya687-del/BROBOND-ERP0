import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="BROBOND ERP | SNBPL", page_icon="⚪", layout="wide")

# --- DATA MANAGEMENT (Your Excel Format) ---
DATA_FILE = "leads_master.csv"
# Aapke exact columns jo aapne bataye hain
EXCEL_COLUMNS = [
    "Lead", "Owner", "First Name", "Last Name", "Email", 
    "Mobile Country Code", "Mobile", "Designation", 
    "Phone Country Code", "Phone", "Lead Source", "Sub Lead Source", 
    "Lead Status", "Industry", "Department", "Annual Revenue", 
    "Company Name", "Country", "State", "City", "Street", 
    "Pincode", "Lead Priority", "Description", "Product Category"
]

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=EXCEL_COLUMNS).to_csv(DATA_FILE, index=False)

# --- STYLING ---
st.markdown("""
    <style>
    .main-header { font-family: 'Helvetica Neue'; color: #1a1a1a; font-weight: 800; font-size: 35px; }
    div.stButton > button { border-radius: 8px; height: 50px; font-weight: 600; width: 100%; }
    [data-testid="stSidebar"] { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<h1 style="text-align:center;">BROBOND</h1>', unsafe_allow_html=True)
    st.write("---")
    if "page" not in st.session_state: st.session_state.page = "Database"
    if st.button("📊 VIEW DATABASE"): st.session_state.page = "Database"
    if st.button("📥 BULK IMPORT EXCEL"): st.session_state.page = "Import"
    if st.button("➕ MANUAL ENTRY"): st.session_state.page = "Entry"

# --- PAGES ---
if st.session_state.page == "Database":
    st.markdown('<div class="main-header">MASTER LEAD DATABASE</div>', unsafe_allow_html=True)
    df = pd.read_csv(DATA_FILE)
    
    # Advanced Search
    search = st.text_input("🔍 Search by Name, Company, or City")
    if search:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    st.dataframe(df, use_container_width=True)

elif st.session_state.page == "Import":
    st.markdown('<div class="main-header">BULK EXCEL IMPORT</div>', unsafe_allow_html=True)
    st.info("Bhai, yahan aap apni 3 products wali Excel files ek-ek karke upload karo.")
    
    prod_name = st.text_input("Enter Product Name (e.g., Classic, Bulk, Sugar-Free)")
    uploaded_file = st.file_uploader("Choose Excel File", type=["xlsx"])
    
    if uploaded_file and prod_name:
        temp_df = pd.read_excel(uploaded_file)
        # Nayi column add kar rahe hain taaki pata chale kaunse product ki lead hai
        temp_df["Product Category"] = prod_name 
        
        st.write(f"Preview of {uploaded_file.name}:")
        st.dataframe(temp_df.head(3))
        
        if st.button("APPEND TO MASTER DATABASE"):
            master_df = pd.read_csv(DATA_FILE)
            final_df = pd.concat([master_df, temp_df], ignore_index=True)
            final_df.to_csv(DATA_FILE, index=False)
            st.success(f"Bhai, {prod_name} ka data successfully add ho gaya!")
            st.balloons()

elif st.session_state.page == "Entry":
    st.markdown('<div class="main-header">NEW LEAD REGISTRATION</div>', unsafe_allow_html=True)
    with st.form("manual_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            fname = st.text_input("First Name")
            lname = st.text_input("Last Name")
            email = st.text_input("Email")
            mob = st.text_input("Mobile")
        with c2:
            comp = st.text_input("Company Name")
            city = st.text_input("City")
            stat = st.selectbox("Lead Status", ["New", "Contacted", "Qualified", "Lost"])
            prio = st.selectbox("Priority", ["High", "Medium", "Low"])
        with c3:
            ind = st.text_input("Industry")
            rev = st.text_input("Annual Revenue")
            prod = st.text_input("Product Category")
            desc = st.text_area("Description")
            
        if st.form_submit_button("SAVE TO ERP"):
            # Yahan hum baki columns ko khali chhod kar main data save karenge
            new_data = pd.DataFrame([[None]*len(EXCEL_COLUMNS)], columns=EXCEL_COLUMNS)
            new_data["First Name"], new_data["Last Name"], new_data["Email"] = fname, lname, email
            new_data["Mobile"], new_data["Company Name"], new_data["City"] = mob, comp, city
            new_data["Lead Status"], new_data["Lead Priority"], new_data["Product Category"] = stat, prio, prod
            new_data["Description"] = desc
            
            new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
            st.success("Entry Saved!")
