import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ["Home", "Data Sertifikat"])

# Display Title and Description
if page == "Home":
    st.title('Website Informasi LPM UNPAR')
    st.markdown('Website ini berisi informasi data internal mengenai Lembaga Penjaminan Mutu (LPM) Universitas Katolik Parahyangan (UNPAR).')
elif page == "Data Sertifikat":
    st.title("Data Sertifikat")

    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)


    def load_data():
        # Fetch existing vendors data
        data = conn.read(worksheet="Data Sertifikat", usecols=list(range(7)), ttl=5)
        return data.dropna(how="all")

    existing_data = load_data()
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

    # Show the form if the button was clicked an odd number of times
    if st.session_state.show_form:
        with st.form(key="data_form"):
            FAKULTAS = st.text_input(label="Fakultas*")
            PRODI_STUDI = st.text_input("Program Studi*")
            PERINGKAT = st.text_input("Peringkat")
            TANGGAL_BERAKHIR = st.date_input(label="Tanggal Berakhir")
            TAHUN = st.text_input(label="Tahun")
            LINK = st.text_input(label="Link")
            PENERBIT = st.selectbox(label="Penerbit", options=TIPE_PENERBIT, index=None)

            st.markdown("*Wajib diisi")

            submit_button = st.form_submit_button(label="Submit Data")

            if submit_button:
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
                st.success("Vendor details successfully submitted!")