import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Form Peminjaman Buku atau Barang LPM", layout="wide")
st.title("Form Peminjaman Buku atau Barang LPM")
st.markdown("Mohon isi data dengan lengkap dan benar. Terima kasih.")
st.caption("🔁 Refresh: Tekan 'R' di komputer atau '⋮' > 'Rerun' di ponsel.")
    
# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data_buku_barang():
    # Fetch existing vendors data
    data = conn.read(worksheet="Data Peminjam Buku atau Barang", usecols=list(range(6)), ttl=5)
    return data.dropna(how="all")

existing_data_buku_barang = load_data_buku_barang()

# Add a text input for filtering
filter_text = st.text_input("Filter data (ketik untuk memfilter)")

# Filter the dataframe based on user input
if filter_text:
    filtered_data_buku = existing_data_buku_barang[existing_data_buku_barang.apply(lambda row: row.astype(str).str.contains(filter_text, case=False).any(), axis=1)]
else:
    filtered_data_buku = existing_data_buku_barang

# Add a new column 'No.' for numbering starting from 1
filtered_data_buku = filtered_data_buku.reset_index(drop=True)
filtered_data_buku.insert(0, 'No', range(1, len(filtered_data_buku) + 1))

# Display the filtered dataframe with the new numbering column
st.dataframe(filtered_data_buku, use_container_width=True, hide_index=True)

# list tipe unit
TIPE_UNIT = [
    "Rektorat",
    "Direktorat Akademik",
    "Direktorat Digitalisasi",
    "Direktorat Kemahasiswaan",
    "Direktorat Manajemen Aset, Keuangan, Dan Sarana Prasarana",
    "Direktorat Organisasi dan Sumber Daya Insani",
    "Direktorat Pemelajaran",
    "Direktorat Pengelolaan Bisnis, Inovasi dan Kewirausahaan",
    "Direktorat Perencanaan Strategis dan Pemasaran",
    "Direktorat Urusan Internasional, Kerja Sama, dan Alumni",
    "Fakultas Ekonomi",
    "Fakultas Filsafat",
    "Fakultas Hukum",
    "Fakultas Ilmu Sosial dan Ilmu Politik",
    "Fakultas Kedokteran",
    "Fakultas Keguruan dan Ilmu Pendidikan",
    "Fakultas Teknik",
    "Fakultas Teknologi Rekayasa",
    "Fakultas Sains",
    "Fakultas Vokasi",
    "Kantor Legal",
    "Kantor Media Digital",
    "Kantor Sekretariat Rektorat",
    "Lembaga Penelitian dan Pengabdian kepada Masyarakat",
    "Lembaga Pengembangan Humaniora",
    "Lembaga Penjaminan Mutu",
    "Perpustakaan",
    "Unit Manajemen Risiko"
]

# Initialize the session state for showing/hiding the form
if 'show_form_buku_barang' not in st.session_state:
    st.session_state.show_form_buku_barang = False

# Toggle the form visibility when the button is clicked
if st.button("Tambah Data"):
    st.session_state.show_form_buku_barang = not st.session_state.show_form_buku_barang
    st.session_state.show_form_sertifikat = False
    st.session_state.show_form_ami = False

# Show the form if authenticated
if st.session_state.show_form_buku_barang:
    with st.form(key="data_form_buku", clear_on_submit=True):
        EMAIL = st.text_input(label="Email*")
        NAMA_PEMINJAM = st.text_input("Nama Peminjam*")
        UNIT = st.selectbox(label="Unit*", options=TIPE_UNIT, index=None)
        NAMA_BUKU_BARANG = st.text_input(label="Nama Buku/Barang*")
        TANGGAL_PINJAM = st.date_input(label="Tanggal Pinjam*")
        TANGGAL_KEMBALI = st.date_input(label="Tanggal Kembali*")

        st.markdown("*Wajib diisi")

        submit_button = st.form_submit_button(label="Submit Data")

        if submit_button:
            if EMAIL and NAMA_PEMINJAM and UNIT and NAMA_BUKU_BARANG and TANGGAL_PINJAM and TANGGAL_KEMBALI:  # Check if required fields are filled
                new_data = pd.DataFrame({
                    "Email": [EMAIL],
                    "Nama Peminjam": [NAMA_PEMINJAM],
                    "Unit": [UNIT],
                    "Nama Buku/Barang": [NAMA_BUKU_BARANG],
                    "Tanggal Pinjam": [TANGGAL_PINJAM],
                    "Tanggal Kembali": [TANGGAL_KEMBALI],
                })
                # Ambil data yang sudah ada dari Google Sheets
                existing_data_buku_barang = conn.read(worksheet="Data Peminjam Buku atau Barang")
                
                # Pastikan hanya kolom 0-5 yang akan diperbarui
                updated_df = existing_data_buku_barang.iloc[:, :6]  # Ambil kolom 0-5 dari data yang sudah ada
                updated_df = pd.concat([updated_df, new_data], ignore_index=True)  # Gabungkan data baru
                
                # Gabungkan kembali dengan kolom 6 ke atas yang tidak akan diubah
                full_data = pd.concat([updated_df, existing_data_buku_barang.iloc[:, 6:]], axis=1)

                # Update hanya kolom 0-5, tetapi tetap mempertahankan kolom 6 ke atas
                conn.update(worksheet="Data Peminjam Buku atau Barang", data=full_data)
                
                st.success("Data berhasil disimpan!")
            else:
                st.error("Gagal menyimpan. Pastikan semua field yang wajib diisi telah terisi.")