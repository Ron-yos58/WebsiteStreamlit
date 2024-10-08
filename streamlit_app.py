import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_option_menu import option_menu
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
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Data Sertifikat Akreditasi", "Data AMI Program Studi", "Form Peminjaman Buku LPM"],
        icons=["house", "book", "book", "journal-check"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"font-size": "12px"},
            "icon": {"font-size": "12px"},
            "nav-link": {"font-size": "12px"},
        }
    )

# Display Title and Description
if selected == "Home":
    st.markdown(
    """
    <div style="text-align: center;">
        <h1>Website Informasi LPM UNPAR</h1>
        Website ini berisi informasi data internal mengenai Lembaga Penjaminan Mutu (LPM) Universitas Katolik Parahyangan (UNPAR).
    </div>
    """,
    unsafe_allow_html=True
)
elif selected == "Data Sertifikat Akreditasi":
    st.title("Data Sertifikat Akreditasi")
    st.markdown('Berikut dibawah ini adalah data sertifikat akreditasi program studi yang dimiliki oleh Universitas Katolik Parahyangan (UNPAR) dari tahun 1998.')
    st.code("Refresh: Tekan 'R' di komputer. Di ponsel: Klik '⋮' > 're-run'.")

    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    def load_data_sertifikat():
        # Fetch existing vendors data
        data = conn.read(worksheet="Data Sertifikat", usecols=list(range(8)), ttl=5)
        return data.dropna(how="all")
     
    existing_data = load_data_sertifikat()

    # Add a text input for filtering
    filter_text = st.text_input("Filter data (ketik untuk memfilter)")
    
    # Filter the dataframe based on user input
    if filter_text:
        filtered_data = existing_data[existing_data.apply(lambda row: row.astype(str).str.contains(filter_text, case=False).any(), axis=1)]
    else:
        filtered_data = existing_data
    
    # Add a new column 'No.' for numbering starting from 1
    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.insert(0, 'No', range(1, len(filtered_data) + 1))
    
    # Display the filtered dataframe with the new numbering column
    st.dataframe(filtered_data, use_container_width=True, hide_index=True)
    
    TIPE_PENERBIT = [
        "BAN-PT",
        "LAM-MEMBA",
        "LAM-PTKes",
        "LAM-TEKNIK",
        "LAM-SAMA"
    ]

    # Initialize the session state for showing/hiding the form
    if 'show_form_sertifikat' not in st.session_state:
        st.session_state.show_form_sertifikat = False

    # Toggle the form visibility when the button is clicked
    if st.button("Tambah Data"):
        st.session_state.show_form_sertifikat = not st.session_state.show_form_sertifikat
        st.session_state.show_form_ami = False
        st.session_state.show_form_buku = False
        
    # Authentication before showing the form
    if st.session_state.show_form_sertifikat and not st.session_state.authenticated:
        password = st.text_input("Masukkan password", type="password", key="password")
        if st.button("Submit Password"):
            check_password()

    # Show the form if authenticated
    if st.session_state.show_form_sertifikat and st.session_state.authenticated:
        with st.form(key="data_form_sertifikat", clear_on_submit=True):
            FAKULTAS = st.text_input(label="Fakultas*")
            PRODI_STUDI = st.text_input("Program Studi*")
            PERINGKAT = st.text_input("Peringkat*")
            TANGGAL_BERAKHIR = st.date_input(label="Tanggal Berakhir*")
            TAHUN = st.text_input(label="Tahun*")
            ISK = st.text_input(label="ISK")
            LINK = st.text_input(label="Link*")
            PENERBIT = st.selectbox(label="Penerbit*", options=TIPE_PENERBIT, index=None)

            st.markdown("*Wajib diisi")

            submit_button = st.form_submit_button(label="Submit Data")

            if submit_button:
                if FAKULTAS and PRODI_STUDI and PERINGKAT and TANGGAL_BERAKHIR and TAHUN and ISK and LINK and PENERBIT:  # Check if required fields are filled
                    new_data = pd.DataFrame({
                        "Fakultas": [FAKULTAS],
                        "Program Studi": [PRODI_STUDI],
                        "Peringkat": [PERINGKAT],
                        "Tanggal Berakhir": [TANGGAL_BERAKHIR],
                        "Tahun": [TAHUN],
                        "ISK": [ISK],
                        "Link": [LINK],
                        "Penerbit": [PENERBIT]
                    })
                    updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                    conn.update(worksheet="Data Sertifikat", data=updated_df)
                    st.success("Data berhasil disimpan!")
                else:
                    st.error("Gagal menyimpan. Pastikan semua field yang wajib diisi telah terisi.")
                    
elif selected == "Data AMI Program Studi":
    st.title('Data AMI Program Studi')
    st.markdown('Berikut dibawah ini adalah data sertifikat Audit Mutu Internal (AMI) program studi yang dimiliki oleh Universitas Katolik Parahyangan (UNPAR) dari tahun 2021.')
    st.code("Refresh: Tekan 'R' di komputer. Di ponsel: Klik '⋮' > 're-run'.")
        
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    def load_data_AMI():
        # Fetch existing vendors data
        data = conn.read(worksheet="Data AMI", usecols=list(range(7)), ttl=5)
        return data.dropna(how="all")

    existing_data_AMI = load_data_AMI()
    
    # Add a text input for filtering
    filter_text = st.text_input("Filter data (ketik untuk memfilter)")
    
    # Filter the dataframe based on user input
    if filter_text:
        filtered_data_ami = existing_data_AMI[existing_data_AMI.apply(lambda row: row.astype(str).str.contains(filter_text, case=False).any(), axis=1)]
    else:
        filtered_data_ami = existing_data_AMI
    
    # Add a new column 'No.' for numbering starting from 1
    filtered_data_ami = filtered_data_ami.reset_index(drop=True)
    filtered_data_ami.insert(0, 'No', range(1, len(filtered_data_ami) + 1))
    
    # Display the filtered dataframe with the new numbering column
    st.dataframe(filtered_data_ami, use_container_width=True, hide_index=True)
    
    # Initialize the session state for showing/hiding the form
    if 'show_form_ami' not in st.session_state:
        st.session_state.show_form_ami = False

    # Toggle the form visibility when the button is clicked
    if st.button("Tambah Data"):
        st.session_state.show_form_ami = not st.session_state.show_form_ami
        st.session_state.show_form_sertifikat = False
        st.session_state.show_form_buku = False
            
    # Authentication before showing the form
    if st.session_state.show_form_ami and not st.session_state.authenticated:
        password = st.text_input("Masukkan password", type="password", key="password")
        if st.button("Submit Password"):
            check_password()

    # Show the form if authenticated
    if st.session_state.show_form_ami and st.session_state.authenticated:
        with st.form(key="data_form_ami", clear_on_submit=True):
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

# page data buku
elif selected == "Form Peminjaman Buku LPM":
    st.title('Form Peminjaman Buku LPM')
    st.markdown('Mohon isi data dengan lengkap dan benar. Terima kasih')
    st.code("Refresh: Tekan 'R' di komputer. Di ponsel: Klik '⋮' > 're-run'.")
    
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    def load_data_buku():
        # Fetch existing vendors data
        data = conn.read(worksheet="Data Peminjam Buku", usecols=list(range(6)), ttl=5)
        return data.dropna(how="all")
    
    existing_data_buku = load_data_buku()
    
    # Add a text input for filtering
    filter_text = st.text_input("Filter data (ketik untuk memfilter)")
    
    # Filter the dataframe based on user input
    if filter_text:
        filtered_data_buku = existing_data_buku[existing_data_buku.apply(lambda row: row.astype(str).str.contains(filter_text, case=False).any(), axis=1)]
    else:
        filtered_data_buku = existing_data_buku
    
    # Add a new column 'No.' for numbering starting from 1
    filtered_data_buku = filtered_data_buku.reset_index(drop=True)
    filtered_data_buku.insert(0, 'No', range(1, len(filtered_data_buku) + 1))
    
    # Display the filtered dataframe with the new numbering column
    st.dataframe(filtered_data_buku, use_container_width=True, hide_index=True)

    
    TIPE_UNIT = [
    "Rektorat",
    "Kantor Sekretariat Rektorat",
    "Kantor Media Digital",
    "Kantor Legal",
    "Lembaga Penjaminan Mutu",
    "Lembaga Pengembangan Humaniora",
    "Lembaga Penelitian dan Pengabdian kepada Masyarakat",
    "Perpustakaan",
    "Unit Manajemen Risiko",
    "Direktorat Akademik",
    "Direktorat Pemelajaran",
    "Direktorat Perencanaan Strategis dan Pemasaran",
    "Direktorat Pengelolaan Bisnis, Inovasi dan Kewirausahaan",
    "Direktorat Kemahasiswaan",
    "Direktorat Digitalisasi",
    "Direktorat Urusan Internasional, Kerja Sama, dan Alumni",
    "Direktorat Organisasi dan Sumber Daya Insani",
    "Direktorat Manajemen Aset, Keuangan, Dan Sarana Prasarana",
    "Fakultas Ekonomi",
    "Fakultas Hukum",
    "Fakultas Ilmu Sosial dan Ilmu Politik",
    "Fakultas Teknik",
    "Fakultas Teknologi Industri",
    "Fakultas Filsafat",
    "Fakultas Teknologi Informasi dan Sains",
    "Fakultas Kedokteran",
    "Program Vokasi dan Profesi"
    ]
    
    # Initialize the session state for showing/hiding the form
    if 'show_form_buku' not in st.session_state:
        st.session_state.show_form_buku = False

    # Toggle the form visibility when the button is clicked
    if st.button("Tambah Data"):
        st.session_state.show_form_buku = not st.session_state.show_form_buku
        st.session_state.show_form_sertifikat = False
        st.session_state.show_form_ami = False

    # Show the form if authenticated
    if st.session_state.show_form_buku:
        with st.form(key="data_form_buku", clear_on_submit=True):
            EMAIL = st.text_input(label="Email*")
            NAMA_PEMINJAM = st.text_input("Nama Peminjam*")
            UNIT = st.selectbox(label="Unit*", options=TIPE_UNIT, index=None)
            JUDUL_BUKU = st.text_input(label="Judul Buku*")
            TANGGAL_PINJAM = st.date_input(label="Tanggal Pinjam*")
            TANGGAL_KEMBALI = st.date_input(label="Tanggal Kembali*")

            st.markdown("*Wajib diisi")

            submit_button = st.form_submit_button(label="Submit Data")

            if submit_button:
                if EMAIL and NAMA_PEMINJAM and UNIT and JUDUL_BUKU and TANGGAL_PINJAM and TANGGAL_KEMBALI:  # Check if required fields are filled
                    new_data = pd.DataFrame({
                        "Email": [EMAIL],
                        "Nama Peminjam": [NAMA_PEMINJAM],
                        "Unit": [UNIT],
                        "Judul Buku": [JUDUL_BUKU],
                        "Tanggal Pinjam": [TANGGAL_PINJAM],
                        "Tanggal Kembali": [TANGGAL_KEMBALI],
                    })
                    # Ambil data yang sudah ada dari Google Sheets
                    existing_data_buku = conn.read(worksheet="Data Peminjam Buku")
                    
                    # Pastikan hanya kolom 0-5 yang akan diperbarui
                    updated_df = existing_data_buku.iloc[:, :6]  # Ambil kolom 0-5 dari data yang sudah ada
                    updated_df = pd.concat([updated_df, new_data], ignore_index=True)  # Gabungkan data baru
                    
                    # Gabungkan kembali dengan kolom 6 ke atas yang tidak akan diubah
                    full_data = pd.concat([updated_df, existing_data_buku.iloc[:, 6:]], axis=1)

                    # Update hanya kolom 0-5, tetapi tetap mempertahankan kolom 6 ke atas
                    conn.update(worksheet="Data Peminjam Buku", data=full_data)
                    
                    st.success("Data berhasil disimpan!")
                else:
                    st.error("Gagal menyimpan. Pastikan semua field yang wajib diisi telah terisi.")