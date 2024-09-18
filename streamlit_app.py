import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Function to check password
def check_password():
    if st.session_state.get('password') == "adminlpm123":
        st.session_state.authenticated = True
        return True
    else:
        st.error("Password salah. Silakan coba lagi.")
        return False

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ["Home", "Data Sertifikat Akreditasi", "Data AMI Program Studi"])

# Display Title and Description
if page == "Home":
    st.title('Website Informasi LPM UNPAR')
    st.markdown('Website ini berisi informasi data internal mengenai Lembaga Penjaminan Mutu (LPM) Universitas Katolik Parahyangan (UNPAR).')
elif page == "Data Sertifikat Akreditasi":
    st.title("Data Sertifikat Akreditasi")
    st.markdown('Berikut dibawah ini adalah data sertifikat akreditasi program studi yang dimiliki oleh Universitas Katolik Parahyangan (UNPAR) dari tahun 1998.')
    st.code("Refresh halaman untuk melihat data terbaru klik tombol 'R'")

    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    def load_data_sertifikat():
        # Fetch existing vendors data
        data = conn.read(worksheet="Data Sertifikat", usecols=list(range(7)), ttl=5)
        return data.dropna(how="all")

    existing_data = load_data_sertifikat()
    st.dataframe(existing_data)

    TIPE_PENERBIT = [
        "BAN-PT",
        "LAM-MEMBA",
        "LAM-PTKes",
        "LAM-TEKNIK",
        "LAM-SAMA"
    ]

    # Initialize the session state for showing/hiding the form
    if 'show_form' not in st.session_state:
        st.session_state.show_form = False

    # Toggle the form visibility when the button is clicked
    if st.button("Tambah Data"):
        st.session_state.show_form = not st.session_state.show_form
        
    # Authentication before showing the form
    if st.session_state.show_form and not st.session_state.authenticated:
        password = st.text_input("Masukkan password", type="password", key="password")
        if st.button("Submit Password"):
            check_password()

    # Show the form if authenticated
    if st.session_state.show_form and st.session_state.authenticated:
        with st.form(key="data_form",clear_on_submit=True):
            FAKULTAS = st.text_input(label="Fakultas*")
            PRODI_STUDI = st.text_input("Program Studi*")
            PERINGKAT = st.text_input("Peringkat*")
            TANGGAL_BERAKHIR = st.date_input(label="Tanggal Berakhir*")
            TAHUN = st.text_input(label="Tahun*")
            LINK = st.text_input(label="Link*")
            PENERBIT = st.selectbox(label="Penerbit*", options=TIPE_PENERBIT, index=None)

            st.markdown("*Wajib diisi")

            submit_button = st.form_submit_button(label="Submit Data")

            if submit_button:
                if FAKULTAS and PRODI_STUDI and PERINGKAT and TANGGAL_BERAKHIR and TAHUN and LINK and PENERBIT:  # Check if required fields are filled
                    new_data = pd.DataFrame({
                        "Fakultas": [FAKULTAS],
                        "Program Studi": [PRODI_STUDI],
                        "Peringkat": [PERINGKAT],
                        "Tanggal Berakhir": [TANGGAL_BERAKHIR],
                        "Tahun": [TAHUN],
                        "Link": [LINK],
                        "Penerbit": [PENERBIT]
                    })
                    updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                    conn.update(worksheet="Data Sertifikat", data=updated_df)
                    st.success("Data berhasil disimpan!")
                else:
                    st.error("Gagal menyimpan. Pastikan semua field yang wajib diisi telah terisi.")

# page data ami
elif page == "Data AMI Program Studi":
    st.title('Data AMI Program Studi')
    st.markdown('Berikut dibawah ini adalah data sertifikat Audit Mutu Internal (AMI) program studi yang dimiliki oleh Universitas Katolik Parahyangan (UNPAR) dari tahun 2021.')
    st.code("Refresh halaman untuk melihat data terbaru klik tombol 'R'")
    
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    def load_data_AMI():
        # Fetch existing vendors data
        data = conn.read(worksheet="Data AMI", usecols=list(range(7)), ttl=5)
        return data.dropna(how="all")

    existing_data_AMI = load_data_AMI()
    st.dataframe(existing_data_AMI)
    
    # Initialize the session state for showing/hiding the form
    if 'show_form' not in st.session_state:
        st.session_state.show_form = False

    # Toggle the form visibility when the button is clicked
    if st.button("Tambah Data"):
        st.session_state.show_form = not st.session_state.show_form
            
    # Authentication before showing the form
    if st.session_state.show_form and not st.session_state.authenticated:
        password = st.text_input("Masukkan password", type="password", key="password")
        if st.button("Submit Password"):
            check_password()

    # Show the form if authenticated
    if st.session_state.show_form and st.session_state.authenticated:
        with st.form(key="data_form", clear_on_submit=True):
            FAKULTAS = st.text_input(label="Fakultas*")
            PRODI_STUDI = st.text_input("Program Studi*")
            TANGGAL = st.date_input(label="Tanggal*")
            TAHUN = st.text_input(label="Tahun*")
            LINK = st.text_input(label="Link*")

            st.markdown("*Wajib diisi")

            submit_button = st.form_submit_button(label="Submit Data")

            if submit_button:
                if FAKULTAS and PRODI_STUDI and TANGGAL and TAHUN and LINK:  # Check if required fields are filled
                    new_data = pd.DataFrame({
                        "Fakultas": [FAKULTAS],
                        "Program Studi": [PRODI_STUDI],
                        "Tanggal": [TANGGAL],
                        "Tahun": [TAHUN],
                        "Link": [LINK],
                    })
                    updated_df = pd.concat([existing_data_AMI, new_data], ignore_index=True)
                    conn.update(worksheet="Data AMI", data=updated_df)
                    st.success("Data berhasil disimpan!")
                else:
                    st.error("Gagal menyimpan. Pastikan semua field yang wajib diisi telah terisi.")

